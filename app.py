# app.py - UniSync Student Resource Hub
# Rewritten to match UNISYNC.sql schema (Java backend compatible)
# Schema uses: Student(SRN, Name, Email, Phone, Password, Dept, Suspended)
#              Resource(ResourceId, Title, Description, ItemCondition, Status, ListingType, OwnerId, CategoryId)
#              Transaction(TransactionId, TransactionType, Status)
#              BuySellTransaction(TransactionId, ResourceId, SellerId, BuyerId, Price)
#              LendBorrowTransaction(TransactionId, ResourceId, LenderId, BorrowerId, StartDate, EndDate, Penalty)
#              BarterTransaction(TransactionId, OfferedResourceId, RequestedResourceId, ProposerId, AccepterId)
#              Review(ReviewId, Rating, Comment, ReviewerId, ResourceId)
#              Reminder(ReminderId, Message, Status, ReminderDate, StudentId, TransactionId)
#              Category(CategoryId, MainType, SubType)

import requests

API_BASE = "http://localhost:8080"

def fetch_resources():
    try:
        res = requests.get(f"{API_BASE}/resources")
        if res.status_code == 200:
            return res.json().get("data", [])
        else:
            st.error("Failed to fetch resources from API")
            return []
    except Exception as e:
        st.error(f"API Error: {e}")
        return []
    
import streamlit as st
import mysql.connector
from datetime import datetime, date
import pandas as pd
import os
from pathlib import Path

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UniSync",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Aesthetic CSS (preserves original style) ─────────────────────────────────
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1C1917;
    }
    [data-testid="stSidebar"] * {
        color: #D6D3D1 !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent;
        border: 1px solid #44403C;
        color: #D6D3D1 !important;
        width: 100%;
        text-align: left;
        border-radius: 8px;
        margin-bottom: 4px;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #292524;
        border-color: #C2622A;
    }
    /* Accent color for primary buttons */
    .stButton > button[kind="primary"] {
        background-color: #C2622A;
        border: none;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #A8521F;
    }
    /* Cards */
    [data-testid="stHorizontalBlock"] > div {
        border-radius: 10px;
    }
    /* Hide streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    /* Tags/badges */
    .tag-sell   { background:#7C3AED; color:white; padding:2px 10px; border-radius:20px; font-size:12px; }
    .tag-lend   { background:#0369A1; color:white; padding:2px 10px; border-radius:20px; font-size:12px; }
    .tag-barter { background:#C2622A; color:white; padding:2px 10px; border-radius:20px; font-size:12px; }
    .tag-avail  { background:#16A34A; color:white; padding:2px 10px; border-radius:20px; font-size:12px; }
    .uni-title  { font-size:2.4rem; font-weight:800; color:#1C1917; letter-spacing:-1px; }
    .uni-accent { color:#C2622A; }
</style>
""", unsafe_allow_html=True)

# ─── Config & Constants ───────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DEPARTMENTS = ['CSE', 'ECE', 'ME', 'Civil', 'EE', 'Other']

# DB credentials — read from .streamlit/secrets.toml
try:
    DB_HOST     = st.secrets["mysql"]["host"]
    DB_USER     = st.secrets["mysql"]["user"]
    DB_PASSWORD = st.secrets["mysql"]["password"]
    DB_NAME     = st.secrets["mysql"]["database"]
except (KeyError, AttributeError):
    DB_HOST = DB_USER = DB_PASSWORD = DB_NAME = None

# ─── Session state ────────────────────────────────────────────────────────────
for key, default in {
    'logged_in_srn': None,
    'page': 'landing',
    'history': ['landing'],
    'barter_proposed': False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Navigation ───────────────────────────────────────────────────────────────
def navigate_to(page_name):
    st.session_state.barter_proposed = False
    if not st.session_state.history or st.session_state.history[-1] != page_name:
        st.session_state.history.append(page_name)
    st.session_state.page = page_name
    st.rerun()

def go_back():
    st.session_state.barter_proposed = False
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()
        prev = st.session_state.history.pop()
        navigate_to(prev)
    else:
        navigate_to('home' if st.session_state.logged_in_srn else 'landing')

def render_back_button():
    if st.session_state.page not in ['landing', 'home']:
        if st.button("⬅️ Go Back", key="back_btn"):
            go_back()

# ─── DB helpers ───────────────────────────────────────────────────────────────
def get_db_connection():
    if DB_HOST is None:
        st.error("🚨 No DB credentials. Add them to `.streamlit/secrets.toml`.")
        return None
    try:
        return mysql.connector.connect(
            host=DB_HOST, user=DB_USER,
            password=DB_PASSWORD, database=DB_NAME
        )
    except mysql.connector.Error as err:
        st.error(f"DB Connection Error: {err}")
        return None

def save_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return None
    ext = Path(uploaded_file.name).suffix
    fname = f"{Path(uploaded_file.name).stem}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
    fpath = UPLOAD_DIR / fname
    try:
        with open(fpath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return str(Path("static") / "images" / fname)
    except Exception as e:
        st.error(f"File save error: {e}")
        return None

# ─── 0. Landing Page ──────────────────────────────────────────────────────────
def page_landing():
    st.markdown('<p class="uni-title">Uni<span class="uni-accent">Sync</span></p>', unsafe_allow_html=True)
    st.subheader("The student resource exchange platform.")
    st.markdown("Buy · Sell · Lend · Borrow · Barter — with your campus community.")
    st.markdown("---")
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        if st.button("Log In", use_container_width=True, type="primary"):
            navigate_to('login')
    with col2:
        if st.button("Sign Up", use_container_width=True):
            navigate_to('signup')

# ─── 1. Login Page ────────────────────────────────────────────────────────────
# def page_login():
#     if st.button("⬅️ Back to Landing", key="login_back"):
#         navigate_to('landing')

#     st.title("Sign in to UniSync")

#     # Toggle: Student / Admin
#     role = st.radio("Role", ["Student", "Admin"], horizontal=True)

#     with st.form("login_form"):
#         login_id  = st.text_input("SRN or Email" if role == "Student" else "Admin Email")
#         login_pwd = st.text_input("Password", type="password")
#         submitted = st.form_submit_button("Sign In", type="primary")

#         if submitted:
#             if not login_id or not login_pwd:
#                 st.warning("Please fill in both fields.")
#                 return

#             conn = get_db_connection()
#             if not conn:
#                 return

#             cursor = conn.cursor(dictionary=True)

#             if role == "Admin":
#                 cursor.execute(
#                     "SELECT AdminId, Password FROM Admin WHERE Email = %s",
#                     (login_id,)
#                 )
#                 admin = cursor.fetchone()
#                 cursor.close(); conn.close()

#                 if admin and admin['Password'] == login_pwd:
#                     st.session_state.logged_in_srn  = f"ADMIN::{admin['AdminId']}"
#                     navigate_to('admin')
#                 else:
#                     st.error("Invalid admin credentials.")
#             else:
#                 cursor.execute(
#                     "SELECT SRN, Password, Suspended FROM Student WHERE SRN = %s OR Email = %s",
#                     (login_id, login_id)
#                 )
#                 user = cursor.fetchone()
#                 cursor.close(); conn.close()

#                 if not user:
#                     st.error("No account found for that SRN/Email.")
#                 elif user['Suspended']:
#                     st.error("Your account has been suspended. Contact admin.")
#                 elif user['Password'] != login_pwd:
#                     st.error("Incorrect password.")
#                 else:
#                     st.session_state.logged_in_srn = user['SRN']
#                     navigate_to('home')

#     st.markdown("**Don't have an account?**")
#     if st.button("Go to Sign Up", key="login_to_signup"):
#         navigate_to('signup')
def page_login():
    if st.button("⬅️ Back to Landing", key="login_back"):
        navigate_to('landing')

    st.title("Sign in to UniSync")

    # Toggle: Student / Admin
    role = st.radio("Role", ["Student", "Admin"], horizontal=True)

    with st.form("login_form"):
        login_id  = st.text_input("SRN or Email" if role == "Student" else "Admin Email")
        login_pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", type="primary")

        if submitted:
            if not login_id or not login_pwd:
                st.warning("Please fill in both fields.")
                return

            # 🔥 ADMIN (keep DB or skip for now)
            if role == "Admin":
                st.warning("Admin login not yet moved to API.")
                return

            # 🔥 STUDENT LOGIN → API CALL
            try:
                res = requests.post(
                    "http://localhost:8080/login",
                    json={
                        "email": login_id,   # your backend expects email
                        "password": login_pwd
                    }
                )

                if res.status_code == 200:
                    data = res.json()
                    st.session_state.logged_in_srn = data["srn"]
                    navigate_to('home')
                else:
                    st.error("Invalid credentials")

            except Exception as e:
                st.error(f"API Error: {e}")

    st.markdown("**Don't have an account?**")
    if st.button("Go to Sign Up", key="login_to_signup"):
        navigate_to('signup')

# ─── 2. Signup Page ───────────────────────────────────────────────────────────
# def page_signup():
#     render_back_button()
#     st.title("Create your UniSync account")

#     with st.form("signup_form"):
#         col1, col2 = st.columns(2)
#         srn   = col1.text_input("SRN (e.g. PES2UG23CS001)", max_chars=20)
#         name  = col2.text_input("Full Name")
#         email = st.text_input("Email")
#         phone = st.text_input("Phone Number", max_chars=15)
#         dept  = st.selectbox("Department", DEPARTMENTS)
#         pwd   = st.text_input("Password", type="password")
#         cpwd  = st.text_input("Confirm Password", type="password")
#         submitted = st.form_submit_button("Create Account", type="primary")

#         if submitted:
#             if not all([srn, name, email, phone, dept, pwd]):
#                 st.warning("All fields are required.")
#                 return
#             if pwd != cpwd:
#                 st.error("Passwords don't match.")
#                 return

#             conn = get_db_connection()
#             if conn:
#                 try:
#                     cursor = conn.cursor()
#                     cursor.execute(
#                         "INSERT INTO Student (SRN, Name, Email, Phone, Password, Dept) "
#                         "VALUES (%s, %s, %s, %s, %s, %s)",
#                         (srn, name, email, phone, pwd, dept)
#                     )
#                     conn.commit()
#                     st.session_state.logged_in_srn = srn
#                     navigate_to('home')
#                 except mysql.connector.Error as err:
#                     st.error(f"Sign-up failed: SRN or Email may already exist. ({err})")
#                 finally:
#                     cursor.close(); conn.close()

#     st.markdown("**Already have an account?**")
#     if st.button("Go to Log In", key="signup_to_login"):
#         navigate_to('login')

def page_signup():
    render_back_button()
    st.title("Create your UniSync account")

    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        srn   = col1.text_input("SRN (e.g. PES2UG23CS001)", max_chars=20)
        name  = col2.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number", max_chars=15)
        dept  = st.selectbox("Department", DEPARTMENTS)
        pwd   = st.text_input("Password", type="password")
        cpwd  = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account", type="primary")

        if submitted:
            if not all([srn, name, email, phone, dept, pwd]):
                st.warning("All fields are required.")
                return

            if pwd != cpwd:
                st.error("Passwords don't match.")
                return

            # 🔥 SIGNUP → API CALL
            try:
                res = requests.post(
                    "http://localhost:8080/signup",
                    json={
                        "id": srn,
                        "name": name,
                        "email": email,
                        "password": pwd,
                        "phone": phone,
                        "dept": dept
                    }
                )

                if res.status_code == 200:
                    st.success("Account created successfully!")
                    st.session_state.logged_in_srn = srn
                    navigate_to('home')
                else:
                    st.error("Signup failed (User may already exist)")

            except Exception as e:
                st.error(f"API Error: {e}")

    st.markdown("**Already have an account?**")
    if st.button("Go to Log In", key="signup_to_login"):
        navigate_to('login')

# ─── Sidebar (for authenticated pages) ───────────────────────────────────────
def render_sidebar(is_admin=False):
    srn = st.session_state.logged_in_srn

    with st.sidebar:
        st.markdown(f"### Uni**Sync**")
        st.markdown(f"👤 `{srn}`")
        st.markdown("---")

        if is_admin:
            st.subheader("Admin")
            if st.button("📊 Dashboard", use_container_width=True):
                navigate_to('admin')
        else:
            st.subheader("Navigation")
            if st.button("🏠 Browse Resources", use_container_width=True):
                navigate_to('home')
            if st.button("💸 Sell an Item", use_container_width=True):
                navigate_to('upload_sell')
            if st.button("📚 Lend an Item", use_container_width=True):
                navigate_to('upload_lend')
            if st.button("🔄 Barter an Item", use_container_width=True):
                navigate_to('upload_barter')
            st.markdown("---")
            if st.button("⚙️ My Activity", use_container_width=True):
                navigate_to('my_activity')

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in_srn = None
            st.session_state.page = 'landing'
            st.session_state.history = ['landing']
            st.rerun()

# ─── 3. Home / Browse ─────────────────────────────────────────────────────────
# def page_home_browse():
#     render_sidebar()
#     st.title("Explore Resources")

#     conn = get_db_connection()
#     if not conn:
#         return

#     user_srn = st.session_state.logged_in_srn

#     # ── Filters
#     search = st.text_input("🔍 Search by title or description", "")
#     col1, col2 = st.columns(2)

#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT DISTINCT MainType FROM Category ORDER BY MainType")
#     main_types = [r['MainType'] for r in cursor.fetchall()]
#     cursor.close()

#     selected_cat  = col1.selectbox("Category", ["All"] + main_types)
#     selected_type = col2.selectbox("Listing Type", ["All", "SELL", "LEND", "BARTER"])

#     # ── Build query
#     where = ["r.Status = 'AVAILABLE'", "r.OwnerId != %s"]
#     params = [user_srn]

#     if search:
#         where.append("(r.Title LIKE %s OR r.Description LIKE %s)")
#         params += [f"%{search}%", f"%{search}%"]
#     if selected_cat != "All":
#         where.append("c.MainType = %s")
#         params.append(selected_cat)
#     if selected_type != "All":
#         where.append("r.ListingType = %s")
#         params.append(selected_type)

#     query = f"""
#         SELECT r.ResourceId, r.Title, r.Description, r.ItemCondition,
#                r.ListingType, r.Status,
#                CONCAT(c.MainType, ' / ', c.SubType) AS Category,
#                s.Name AS OwnerName
#         FROM Resource r
#         JOIN Category c ON r.CategoryId = c.CategoryId
#         JOIN Student s  ON r.OwnerId = s.SRN
#         WHERE {' AND '.join(where)}
#         ORDER BY r.CreatedAt DESC
#     """
#     df = pd.read_sql(query, conn, params=params)
#     conn.close()

#     st.markdown("---")
#     st.subheader(f"Available Items ({len(df)})")

#     if df.empty:
#         st.info("No items match your search and filters.")
#         return

#     cols = st.columns(3)
#     for i, row in df.iterrows():
#         lt = row['ListingType'].upper()
#         tag_style = {'SELL': 'tag-sell', 'LEND': 'tag-lend', 'BARTER': 'tag-barter'}.get(lt, 'tag-sell')
#         page_map  = {'SELL': 'buysell',  'LEND': 'lendborrow', 'BARTER': 'barter'}
#         action_page = page_map.get(lt, 'buysell')

#         with cols[i % 3]:
#             with st.container(border=True):
#                 st.markdown(
#                     f"**{row['Title']}** "
#                     f"<span class='{tag_style}'>{lt}</span>",
#                     unsafe_allow_html=True
#                 )
#                 st.caption(f"📂 {row['Category']}  |  🔧 {row['ItemCondition']}")
#                 desc = str(row['Description'] or "")
#                 st.markdown(f"*{desc[:80]}{'...' if len(desc) > 80 else ''}*")
#                 st.caption(f"👤 {row['OwnerName']}")

#                 if st.button(f"View · #{row['ResourceId']}", key=f"act_{row['ResourceId']}", use_container_width=True):
#                     st.session_state['target_resource_id'] = int(row['ResourceId'])
#                     navigate_to(action_page)

def page_home_browse():
    render_sidebar()
    st.title("Explore Resources")

    # 🔥 FETCH FROM JAVA API
    resources = fetch_resources()

    if not resources:
        st.info("No items available.")
        return

    # 🔄 Convert API JSON → DataFrame (same format as before)
    data = []
    for r in resources:
        data.append({
            "ResourceId": r["resourceId"],
            "Title": r["title"],
            "Description": r["description"],
            "ItemCondition": r["condition"],
            "ListingType": r["listingType"],
            "Status": r["status"],
            "Category": f'{r["category"]["mainType"]} / {r["category"]["subType"]}',
            "OwnerName": r["owner"]["name"]
        })

    df = pd.DataFrame(data)

    # 🔍 Filters (UI SAME)
    search = st.text_input("🔍 Search by title or description", "")
    col1, col2 = st.columns(2)

    selected_cat  = col1.selectbox("Category", ["All"] + list(df["Category"].unique()))
    selected_type = col2.selectbox("Listing Type", ["All", "SELL", "LEND", "BARTER"])

    # Apply filters
    if search:
        df = df[df["Title"].str.contains(search, case=False) | df["Description"].str.contains(search, case=False)]

    if selected_cat != "All":
        df = df[df["Category"] == selected_cat]

    if selected_type != "All":
        df = df[df["ListingType"] == selected_type]

    st.markdown("---")
    st.subheader(f"Available Items ({len(df)})")

    if df.empty:
        st.info("No items match your filters.")
        return

    # 🎨 SAME UI CARDS (unchanged)
    cols = st.columns(3)
    for i, row in df.iterrows():
        lt = row['ListingType'].upper()
        tag_style = {'SELL': 'tag-sell', 'LEND': 'tag-lend', 'BARTER': 'tag-barter'}.get(lt, 'tag-sell')
        page_map  = {'SELL': 'buysell',  'LEND': 'lendborrow', 'BARTER': 'barter'}
        action_page = page_map.get(lt, 'buysell')

        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(
                    f"**{row['Title']}** "
                    f"<span class='{tag_style}'>{lt}</span>",
                    unsafe_allow_html=True
                )
                st.caption(f"📂 {row['Category']}  |  🔧 {row['ItemCondition']}")
                desc = str(row['Description'] or "")
                st.markdown(f"*{desc[:80]}{'...' if len(desc) > 80 else ''}*")
                st.caption(f"👤 {row['OwnerName']}")

                if st.button(f"View · #{row['ResourceId']}", key=f"act_{row['ResourceId']}", use_container_width=True):
                    st.session_state['target_resource_id'] = int(row['ResourceId'])
                    navigate_to(action_page)

# ─── 4. Upload / List Item ────────────────────────────────────────────────────
def page_upload_item(action_type):
    render_sidebar()
    render_back_button()

    label_map = {'sell': '💸 Sell', 'lend': '📚 Lend', 'barter': '🔄 Barter'}
    st.header(f"{label_map[action_type]} an Item")
    st.markdown("---")

    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT CategoryId, MainType, SubType FROM Category ORDER BY MainType, SubType")
    categories = cursor.fetchall()
    cursor.close()

    cat_map   = {f"{c['MainType']} / {c['SubType']}": c['CategoryId'] for c in categories}
    cat_names = list(cat_map.keys())

    with st.form(f"upload_{action_type}_form"):
        col_img, col_det = st.columns([1, 2])

        with col_img:
            st.subheader("Image (Optional)")
            uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, use_container_width=True)

        with col_det:
            title       = st.text_input("Item Title *")
            description = st.text_area("Description", height=100)
            condition   = st.selectbox("Condition *", ['Excellent', 'Good', 'Fair', 'Poor'])
            category    = st.selectbox("Category *", cat_names)

            if action_type == 'sell':
                price = st.number_input("Asking Price (₹) *", min_value=1.0, format="%.2f")
                btn_label = "List for Sale"
            elif action_type == 'lend':
                lend_note = st.text_area("Lending Terms (duration, conditions, late-fee info)")
                btn_label = "List for Lending"
            else:  # barter
                barter_pref = st.text_area("What would you like in exchange?")
                btn_label = "List for Barter"

        submitted = st.form_submit_button(btn_label, type="primary")

        if submitted:
            if not title:
                st.error("Title is required.")
                return

            cat_id      = cat_map[category]
            listing_type = action_type.upper()
            image_path  = save_uploaded_file(uploaded_file)
            user_srn    = st.session_state.logged_in_srn

            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Resource (Title, Description, ItemCondition, Status, ListingType, OwnerId, CategoryId) "
                    "VALUES (%s, %s, %s, 'AVAILABLE', %s, %s, %s)",
                    (title, description, condition, listing_type, user_srn, cat_id)
                )
                conn.commit()
                st.success(f"'{title}' listed successfully!")
                navigate_to('home')
            except mysql.connector.Error as err:
                st.error(f"Failed to list item: {err}")
            finally:
                cursor.close()
            conn.close()

# ─── 5. Buy / Sell Page ───────────────────────────────────────────────────────
def page_buysell():
    render_sidebar()
    render_back_button()
    st.header("🤝 Buy / Sell")
    user_srn = st.session_state.logged_in_srn

    tab1, tab2 = st.tabs(["Browse Items to Buy", "My Buy/Sell Transactions"])

    # ── Tab 1: Browse & buy
    with tab1:
        conn = get_db_connection()
        if not conn: return

        target = st.session_state.get('target_resource_id')
        extra_where = f"AND r.ResourceId = {int(target)}" if target else ""

        query = f"""
            SELECT r.ResourceId, r.Title, r.Description, r.ItemCondition,
                   s.Name AS SellerName, s.SRN AS SellerSRN
            FROM Resource r
            JOIN Student s ON r.OwnerId = s.SRN
            WHERE r.Status = 'AVAILABLE'
              AND r.ListingType = 'SELL'
              AND r.OwnerId != %s
              {extra_where}
        """
        df = pd.read_sql(query, conn, params=(user_srn,))
        conn.close()

        if df.empty:
            st.info("No items currently listed for sale.")
        else:
            st.dataframe(df[['ResourceId', 'Title', 'ItemCondition', 'SellerName']], hide_index=True)
            st.markdown("---")
            st.subheader("Initiate Purchase")

            with st.form("buysell_form"):
                resource_id = st.selectbox("Select Resource ID", df['ResourceId'].unique())
                price       = st.number_input("Agreed Price (₹)", min_value=1.0, format="%.2f")
                submitted   = st.form_submit_button("Confirm Purchase", type="primary")

                if submitted:
                    row = df[df['ResourceId'] == resource_id].iloc[0]
                    conn2 = get_db_connection()
                    if conn2:
                        try:
                            cursor = conn2.cursor()
                            # Insert base Transaction row
                            cursor.execute(
                                "INSERT INTO Transaction (TransactionType, Status) VALUES ('BUYSELL', 'PENDING')"
                            )
                            txn_id = cursor.lastrowid
                            # Insert BuySellTransaction detail
                            cursor.execute(
                                "INSERT INTO BuySellTransaction (TransactionId, ResourceId, SellerId, BuyerId, Price) "
                                "VALUES (%s, %s, %s, %s, %s)",
                                (txn_id, resource_id, row['SellerSRN'], user_srn, price)
                            )
                            # Mark resource as unavailable (reserved)
                            cursor.execute(
                                "UPDATE Resource SET Status='RESERVED' WHERE ResourceId=%s",
                                (resource_id,)
                            )
                            conn2.commit()
                            st.session_state['target_resource_id'] = None
                            st.success(f"Purchase initiated! Transaction ID: {txn_id}. Coordinate with seller to complete.")
                            st.rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Transaction failed: {err}")
                        finally:
                            cursor.close(); conn2.close()

    # ── Tab 2: My buy/sell transactions
    with tab2:
        conn = get_db_connection()
        if not conn: return

        query = """
            SELECT t.TransactionId, r.Title, seller.Name AS Seller, buyer.Name AS Buyer,
                   b.Price, t.Status, DATE(t.CreatedAt) AS Date
            FROM BuySellTransaction b
            JOIN Transaction t  ON b.TransactionId = t.TransactionId
            JOIN Resource r     ON b.ResourceId = r.ResourceId
            JOIN Student seller ON b.SellerId = seller.SRN
            JOIN Student buyer  ON b.BuyerId  = buyer.SRN
            WHERE b.SellerId = %s OR b.BuyerId = %s
            ORDER BY t.CreatedAt DESC
        """
        df_txns = pd.read_sql(query, conn, params=(user_srn, user_srn))

        if df_txns.empty:
            st.info("No buy/sell transactions yet.")
        else:
            st.dataframe(df_txns, hide_index=True)

            st.markdown("---")
            pending = df_txns[df_txns['Status'] == 'PENDING']
            if not pending.empty:
                with st.form("complete_buysell_form"):
                    txn_to_complete = st.selectbox("Transaction ID to Mark Completed", pending['TransactionId'].unique())
                    if st.form_submit_button("Mark as Completed", type="primary"):
                        try:
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE Transaction SET Status='COMPLETED' WHERE TransactionId=%s",
                                (txn_to_complete,)
                            )
                            # Trigger in DB marks resource as SOLD, but do it here too for safety
                            cursor.execute(
                                "UPDATE Resource SET Status='SOLD' WHERE ResourceId = "
                                "(SELECT ResourceId FROM BuySellTransaction WHERE TransactionId=%s)",
                                (txn_to_complete,)
                            )
                            conn.commit()
                            st.success(f"Transaction {txn_to_complete} marked completed!")
                            st.rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Error: {err}")
                        finally:
                            cursor.close()
        conn.close()

# ─── 6. Lend / Borrow Page ────────────────────────────────────────────────────
# def page_lendborrow():
#     render_sidebar()
#     render_back_button()
#     st.header("📚 Lend / Borrow")
#     user_srn = st.session_state.logged_in_srn

#     tab1, tab2 = st.tabs(["Borrow an Item", "My Lend/Borrow Transactions"])

    # with tab1:
    #     conn = get_db_connection()
    #     if not conn: return

    #     target = st.session_state.get('target_resource_id')
    #     extra_where = f"AND r.ResourceId = {int(target)}" if target else ""

    #     query = f"""
    #         SELECT r.ResourceId, r.Title, r.Description, r.ItemCondition,
    #                s.Name AS LenderName, s.SRN AS LenderSRN
    #         FROM Resource r
    #         JOIN Student s ON r.OwnerId = s.SRN
    #         WHERE r.Status = 'AVAILABLE'
    #           AND r.ListingType = 'LEND'
    #           AND r.OwnerId != %s
    #           {extra_where}
    #     """
    #     df = pd.read_sql(query, conn, params=(user_srn,))
    #     conn.close()

    #     if df.empty:
    #         st.info("No items available to borrow right now.")
    #     else:
    #         st.dataframe(df[['ResourceId', 'Title', 'ItemCondition', 'LenderName']], hide_index=True)
    #         st.markdown("---")
    #         st.subheader("Request to Borrow")

    #         with st.form("borrow_form"):
    #             resource_id = st.selectbox("Select Resource ID", df['ResourceId'].unique())
    #             start_date  = st.date_input("Start Date", date.today())
    #             end_date    = st.date_input("Planned Return Date", date.today())
    #             submitted   = st.form_submit_button("Initiate Borrow", type="primary")

    #             if submitted:
    #                 if end_date <= start_date:
    #                     st.error("Return date must be after start date.")
    #                     return
    #                 row = df[df['ResourceId'] == resource_id].iloc[0]
    #                 conn2 = get_db_connection()
    #                 if conn2:
    #                     try:
    #                         cursor = conn2.cursor()
    #                         cursor.execute(
    #                             "INSERT INTO Transaction (TransactionType, Status) VALUES ('LENDBORROW', 'PENDING')"
    #                         )
    #                         txn_id = cursor.lastrowid
    #                         cursor.execute(
    #                             "INSERT INTO LendBorrowTransaction "
    #                             "(TransactionId, ResourceId, LenderId, BorrowerId, StartDate, EndDate, Penalty) "
    #                             "VALUES (%s, %s, %s, %s, %s, %s, 0)",
    #                             (txn_id, resource_id, row['LenderSRN'], user_srn, start_date, end_date)
    #                         )
    #                         cursor.execute(
    #                             "UPDATE Resource SET Status='BORROWED' WHERE ResourceId=%s",
    #                             (resource_id,)
    #                         )
    #                         conn2.commit()
    #                         st.session_state['target_resource_id'] = None
    #                         st.success(f"Borrow initiated! Transaction ID: {txn_id}. Coordinate with the lender.")
    #                         st.rerun()
    #                     except mysql.connector.Error as err:
    #                         st.error(f"Failed to initiate borrow: {err}")
    #                     finally:
    #                         cursor.close(); conn2.close()

    # with tab2:
    #     conn = get_db_connection()
    #     if not conn: return

    #     query = """
    #         SELECT t.TransactionId, r.Title, lender.Name AS Lender, borrower.Name AS Borrower,
    #                l.StartDate, l.EndDate, l.Penalty, t.Status,
    #                DATEDIFF(CURDATE(), l.EndDate) AS DaysLate
    #         FROM LendBorrowTransaction l
    #         JOIN Transaction t      ON l.TransactionId = t.TransactionId
    #         JOIN Resource r         ON l.ResourceId = r.ResourceId
    #         JOIN Student lender     ON l.LenderId   = lender.SRN
    #         JOIN Student borrower   ON l.BorrowerId = borrower.SRN
    #         WHERE l.LenderId = %s OR l.BorrowerId = %s
    #         ORDER BY t.CreatedAt DESCA
    #     """
    #     df_loans = pd.read_sql(query, conn, params=(user_srn, user_srn))

    #     if df_loans.empty:
    #         st.info("No lend/borrow transactions yet.")
    #     else:
    #         st.dataframe(df_loans, hide_index=True)

    #         st.markdown("---")
    #         # Show return button only for items borrower is responsible for
    #         ongoing = df_loans[(df_loans['Status'] == 'PENDING') & (df_loans['Borrower'].notna())]
    #         # Filter to only the ones this user is the borrower
    #         borrow_cursor = conn.cursor(dictionary=True)
    #         borrow_cursor.execute(
    #             "SELECT TransactionId FROM LendBorrowTransaction WHERE BorrowerId=%s",
    #             (user_srn,)
    #         )
    #         my_borrows = {r['TransactionId'] for r in borrow_cursor.fetchall()}
    #         borrow_cursor.close()

    #         my_ongoing = df_loans[
    #             (df_loans['Status'] == 'PENDING') &
    #             (df_loans['TransactionId'].isin(my_borrows))
    #         ]

    #         if not my_ongoing.empty:
    #             st.subheader("Return an Item")
    #             with st.form("return_form"):
    #                 return_id = st.selectbox("Loan Transaction ID", my_ongoing['TransactionId'].unique())
    #                 if st.form_submit_button("Confirm Return", type="primary"):
    #                     try:
    #                         cursor = conn.cursor()
    #                         # Calculate penalty for late returns (₹10/day)
    #                         cursor.execute(
    #                             "SELECT EndDate, ResourceId FROM LendBorrowTransaction WHERE TransactionId=%s",
    #                             (return_id,)
    #                         )
    #                         loan_row = cursor.fetchone()
    #                         if loan_row:
    #                             days_late = (date.today() - loan_row[0]).days if date.today() > loan_row[0] else 0
    #                             penalty = max(0, days_late) * 10.0
    #                             cursor.execute(
    #                                 "UPDATE LendBorrowTransaction SET Penalty=%s WHERE TransactionId=%s",
    #                                 (penalty, return_id)
    #                             )
    #                             cursor.execute(
    #                                 "UPDATE Transaction SET Status='COMPLETED' WHERE TransactionId=%s",
    #                                 (return_id,)
    #                             )
    #                             cursor.execute(
    #                                 "UPDATE Resource SET Status='AVAILABLE' WHERE ResourceId=%s",
    #                                 (loan_row[1],)
    #                             )
    #                             conn.commit()
    #                             if penalty > 0:
    #                                 st.warning(f"Returned late! Penalty applied: ₹{penalty:.2f}")
    #                             else:
    #                                 st.success("Item returned on time. Loan completed!")
    #                             st.rerun()
    #                     except mysql.connector.Error as err:
    #                         st.error(f"Return failed: {err}")
    #                     finally:
    #                         cursor.close()

    #     conn.close()
def page_lendborrow():
    render_sidebar()
    render_back_button()
    st.header("📚 Lend / Borrow")

    user_srn = st.session_state.logged_in_srn

    tab1, tab2 = st.tabs(["Borrow an Item", "My Transactions"])

    # =========================
    # 🔥 TAB 1: BORROW
    # =========================
    with tab1:
        resources = fetch_resources()

        # filter only lend items
        lend_items = [r for r in resources if r["listingType"] == "LEND" and r["owner"]["id"] != user_srn]

        if not lend_items:
            st.info("No items available to borrow.")
            return

        data = []
        for r in lend_items:
            data.append({
                "ResourceId": r["resourceId"],
                "Title": r["title"],
                "Condition": r["condition"],
                "LenderName": r["owner"]["name"],
                "LenderSRN": r["owner"]["id"]
            })

        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True)

        st.markdown("---")
        st.subheader("Request to Borrow")

        with st.form("borrow_form"):
            resource_id = st.selectbox("Select Resource", df["ResourceId"])
            start_date = st.date_input("Start Date", date.today())
            end_date = st.date_input("Return Date", date.today())

            submitted = st.form_submit_button("Borrow", type="primary")

            if submitted:
                if end_date <= start_date:
                    st.error("Return date must be after start date.")
                    return

                row = df[df["ResourceId"] == resource_id].iloc[0]

                try:
                    res = requests.post(
                        f"{API_BASE}/borrow",
                        json={
                            "resourceId": int(resource_id),
                            "borrowerId": user_srn,
                            "lenderId": row["LenderSRN"],
                            "startDate": str(start_date),
                            "endDate": str(end_date)
                        }
                    )

                    if res.status_code == 200:
                        st.success("Borrow initiated successfully 🚀")
                        st.rerun()
                    else:
                        st.error("Borrow failed")

                except Exception as e:
                    st.error(f"API Error: {e}")

    # =========================
    # 🔥 TAB 2: RETURN
    # =========================
    with tab2:
        st.subheader("Your Borrowed Items")

        try:
            res = requests.get(f"{API_BASE}/transactions/{user_srn}")

            if res.status_code != 200:
                st.error("Failed to fetch transactions")
                return

            txns = res.json().get("data", [])

        except Exception as e:
            st.error(f"API Error: {e}")
            return

        # filter only active borrow transactions
        active_loans = [t for t in txns if t["type"] == "LENDBORROW" and t["status"] == "PENDING"]

        if not active_loans:
            st.info("No active borrowings.")
            return

        df = pd.DataFrame(active_loans)
        st.dataframe(df, hide_index=True)

        st.markdown("---")
        st.subheader("Return an Item")

        with st.form("return_form"):
            txn_id = st.selectbox("Transaction ID", df["transactionId"])

            submitted = st.form_submit_button("Return Item", type="primary")

            if submitted:
                try:
                    res = requests.post(
                        f"{API_BASE}/return",
                        json={
                            "transactionId": int(txn_id)
                        }
                    )

                    if res.status_code == 200:
                        st.success("Item returned successfully ✅")
                        st.rerun()
                    else:
                        st.error("Return failed")

                except Exception as e:
                    st.error(f"API Error: {e}")
    

# ─── 7. Barter Page ───────────────────────────────────────────────────────────
def page_barter():
    render_sidebar()
    render_back_button()
    st.header("🔄 Barter")
    user_srn = st.session_state.logged_in_srn

    if 'barter_proposed' not in st.session_state:
        st.session_state.barter_proposed = False

    tab1, tab2, tab3 = st.tabs(["Propose a Barter", "Review Proposals", "My Barter History"])

    conn = get_db_connection()
    if not conn: return

    # My barter-listed resources
    my_resources = pd.read_sql(
        "SELECT ResourceId, Title FROM Resource WHERE OwnerId=%s AND Status='AVAILABLE' AND ListingType='BARTER'",
        conn, params=(user_srn,)
    )
    my_res_map   = {f"{r['Title']} (ID:{r['ResourceId']})": r['ResourceId'] for r in my_resources.to_dict('records')}
    conn.close()

    # ── Tab 1: Propose
    with tab1:
        st.subheader("Propose a New Barter")

        if st.session_state.barter_proposed:
            st.success("✅ Barter proposal submitted! The other student will see it in 'Review Proposals'.")
        else:
            if not my_res_map:
                st.info("You need to list at least one item as 'BARTER' before proposing a trade.")
            else:
                conn2 = get_db_connection()
                if not conn2: return

                target = st.session_state.get('target_resource_id')
                extra_where = f"AND r.ResourceId = {int(target)}" if target else ""

                others = pd.read_sql(f"""
                    SELECT r.ResourceId, r.Title, s.Name AS OwnerName, s.SRN AS OwnerSRN
                    FROM Resource r JOIN Student s ON r.OwnerId = s.SRN
                    WHERE r.Status='AVAILABLE' AND r.ListingType='BARTER' AND r.OwnerId != %s
                    {extra_where}
                """, conn2, params=(user_srn,))
                conn2.close()

                if others.empty:
                    st.info("No other barter items available right now.")
                else:
                    other_map = {
                        f"{r['Title']} — {r['OwnerName']} (ID:{r['ResourceId']})": (r['ResourceId'], r['OwnerSRN'])
                        for r in others.to_dict('records')
                    }

                    with st.form("barter_propose_form"):
                        my_item_key    = st.selectbox("Your Item (offering)", list(my_res_map.keys()))
                        their_item_key = st.selectbox("Item You Want", list(other_map.keys()))
                        submitted      = st.form_submit_button("Submit Barter Proposal", type="primary")

                        if submitted:
                            my_res_id           = my_res_map[my_item_key]
                            their_res_id, their_srn = other_map[their_item_key]
                            conn3 = get_db_connection()
                            if conn3:
                                try:
                                    cursor = conn3.cursor()
                                    cursor.execute(
                                        "INSERT INTO Transaction (TransactionType, Status) VALUES ('BARTER', 'PENDING')"
                                    )
                                    txn_id = cursor.lastrowid
                                    cursor.execute(
                                        "INSERT INTO BarterTransaction "
                                        "(TransactionId, OfferedResourceId, RequestedResourceId, ProposerId, AccepterId) "
                                        "VALUES (%s, %s, %s, %s, %s)",
                                        (txn_id, my_res_id, their_res_id, user_srn, their_srn)
                                    )
                                    conn3.commit()
                                    st.session_state.barter_proposed = True
                                    st.session_state['target_resource_id'] = None
                                    st.rerun()
                                except mysql.connector.Error as err:
                                    st.error(f"Barter proposal failed: {err}")
                                finally:
                                    cursor.close(); conn3.close()

    # ── Tab 2: Review incoming proposals
    with tab2:
        st.subheader("Proposals Waiting for Your Response")
        conn4 = get_db_connection()
        if not conn4: return

        proposals = pd.read_sql("""
            SELECT bt.TransactionId, r1.Title AS TheirOffer, r2.Title AS YourItem,
                   proposer.Name AS ProposedBy
            FROM BarterTransaction bt
            JOIN Transaction t      ON bt.TransactionId = t.TransactionId
            JOIN Resource r1        ON bt.OfferedResourceId = r1.ResourceId
            JOIN Resource r2        ON bt.RequestedResourceId = r2.ResourceId
            JOIN Student proposer   ON bt.ProposerId = proposer.SRN
            WHERE bt.AccepterId = %s AND t.Status = 'PENDING'
        """, conn4, params=(user_srn,))

        if proposals.empty:
            st.info("No pending proposals for you.")
        else:
            st.dataframe(proposals, hide_index=True)

            with st.form("barter_review_form"):
                txn_to_review = st.selectbox("Transaction ID to Respond To", proposals['TransactionId'].unique())
                col_a, col_r = st.columns(2)
                accept = col_a.form_submit_button("✅ Accept", type="primary")
                reject = col_r.form_submit_button("❌ Reject")

                if accept or reject:
                    new_status = 'COMPLETED' if accept else 'CANCELLED'
                    try:
                        cursor = conn4.cursor()
                        cursor.execute(
                            "UPDATE Transaction SET Status=%s WHERE TransactionId=%s",
                            (new_status, txn_to_review)
                        )
                        conn4.commit()
                        st.success(f"Proposal {'accepted' if accept else 'rejected'}.")
                        st.rerun()
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
                    finally:
                        cursor.close()
        conn4.close()

    # ── Tab 3: History
    with tab3:
        st.subheader("My Barter History")
        conn5 = get_db_connection()
        if not conn5: return

        history = pd.read_sql("""
            SELECT t.TransactionId, r1.Title AS ItemOffered, r2.Title AS ItemRequested,
                   proposer.Name AS Proposer, accepter.Name AS Accepter,
                   t.Status, DATE(t.CreatedAt) AS Date
            FROM BarterTransaction bt
            JOIN Transaction t    ON bt.TransactionId = t.TransactionId
            JOIN Resource r1      ON bt.OfferedResourceId = r1.ResourceId
            JOIN Resource r2      ON bt.RequestedResourceId = r2.ResourceId
            JOIN Student proposer ON bt.ProposerId = proposer.SRN
            JOIN Student accepter ON bt.AccepterId = accepter.SRN
            WHERE bt.ProposerId = %s OR bt.AccepterId = %s
            ORDER BY t.CreatedAt DESC
        """, conn5, params=(user_srn, user_srn))

        if history.empty:
            st.info("No barter history found.")
        else:
            st.dataframe(history, hide_index=True)
        conn5.close()

# ─── 8. My Activity Page ──────────────────────────────────────────────────────
def page_my_activity():
    render_sidebar()
    render_back_button()
    st.header("⚙️ My Activity")
    user_srn = st.session_state.logged_in_srn

    conn = get_db_connection()
    if not conn: return

    tab1, tab2, tab3, tab4 = st.tabs([
        "My Resources", "My Transactions", "My Loans", "Reviews & Reminders"
    ])

    # ── Tab 1: My listed resources
    with tab1:
        st.subheader("Items I've Listed")
        df_res = pd.read_sql("""
            SELECT r.ResourceId, r.Title, r.ItemCondition, r.Status, r.ListingType,
                   CONCAT(c.MainType,' / ',c.SubType) AS Category
            FROM Resource r JOIN Category c ON r.CategoryId = c.CategoryId
            WHERE r.OwnerId = %s
        """, conn, params=(user_srn,))

        if df_res.empty:
            st.info("You haven't listed anything yet.")
        else:
            st.dataframe(df_res, hide_index=True)

            st.markdown("---")
            available = df_res[df_res['Status'] == 'AVAILABLE']

            # Edit
            st.subheader("📝 Edit a Resource")
            if available.empty:
                st.info("Only 'AVAILABLE' resources can be edited.")
            else:
                edit_id = st.selectbox("Select Resource to Edit", available['ResourceId'].unique(),
                                       key="edit_sel", index=None, placeholder="Choose...")
                if edit_id:
                    ec = conn.cursor(dictionary=True)
                    ec.execute("SELECT Title, Description, ItemCondition, ListingType FROM Resource WHERE ResourceId=%s", (int(edit_id),))
                    rd = ec.fetchone(); ec.close()
                    if rd:
                        conditions    = ['Excellent', 'Good', 'Fair', 'Poor']
                        listing_types = ['SELL', 'LEND', 'BARTER']
                        with st.form("edit_res_form"):
                            new_title = st.text_input("Title", value=rd['Title'])
                            new_desc  = st.text_area("Description", value=rd['Description'] or "")
                            new_cond  = st.selectbox("Condition", conditions,
                                                     index=conditions.index(rd['ItemCondition']) if rd['ItemCondition'] in conditions else 0)
                            new_type  = st.selectbox("Listing Type", listing_types,
                                                     index=listing_types.index(rd['ListingType']) if rd['ListingType'] in listing_types else 0)
                            if st.form_submit_button("Save Changes", type="primary"):
                                if not new_title:
                                    st.error("Title cannot be empty.")
                                else:
                                    try:
                                        uc = conn.cursor()
                                        uc.execute(
                                            "UPDATE Resource SET Title=%s, Description=%s, ItemCondition=%s, ListingType=%s WHERE ResourceId=%s AND OwnerId=%s",
                                            (new_title, new_desc, new_cond, new_type, int(edit_id), user_srn)
                                        )
                                        conn.commit(); uc.close()
                                        st.success("Resource updated!"); st.rerun()
                                    except mysql.connector.Error as err:
                                        st.error(f"Update failed: {err}")

            # Delete
            st.markdown("---")
            st.subheader("🗑️ Delete a Resource")
            if available.empty:
                st.info("Only 'AVAILABLE' resources can be deleted.")
            else:
                del_id = st.selectbox("Select Resource to Delete", available['ResourceId'].unique(), key="del_sel")
                if st.button(f"Permanently Delete Resource #{del_id}", type="primary"):
                    try:
                        dc = conn.cursor()
                        dc.execute("DELETE FROM Resource WHERE ResourceId=%s AND OwnerId=%s", (del_id, user_srn))
                        conn.commit(); dc.close()
                        st.success(f"Resource #{del_id} deleted."); st.rerun()
                    except mysql.connector.Error as err:
                        st.error(f"Delete failed: {err}")

    # ── Tab 2: My buy/sell
    with tab2:
        st.subheader("Buy/Sell Transactions")
        df_bs = pd.read_sql("""
            SELECT t.TransactionId, r.Title, seller.Name AS Seller, buyer.Name AS Buyer,
                   b.Price, t.Status, DATE(t.CreatedAt) AS Date
            FROM BuySellTransaction b
            JOIN Transaction t  ON b.TransactionId = t.TransactionId
            JOIN Resource r     ON b.ResourceId = r.ResourceId
            JOIN Student seller ON b.SellerId = seller.SRN
            JOIN Student buyer  ON b.BuyerId  = buyer.SRN
            WHERE b.SellerId=%s OR b.BuyerId=%s
            ORDER BY t.CreatedAt DESC
        """, conn, params=(user_srn, user_srn))
        st.dataframe(df_bs if not df_bs.empty else pd.DataFrame({"Message": ["No buy/sell transactions."]}), hide_index=True)

        st.subheader("Barter Transactions")
        df_barter = pd.read_sql("""
            SELECT t.TransactionId, r1.Title AS Offered, r2.Title AS Requested,
                   proposer.Name AS Proposer, accepter.Name AS Accepter, t.Status
            FROM BarterTransaction bt
            JOIN Transaction t    ON bt.TransactionId = t.TransactionId
            JOIN Resource r1      ON bt.OfferedResourceId = r1.ResourceId
            JOIN Resource r2      ON bt.RequestedResourceId = r2.ResourceId
            JOIN Student proposer ON bt.ProposerId = proposer.SRN
            JOIN Student accepter ON bt.AccepterId = accepter.SRN
            WHERE bt.ProposerId=%s OR bt.AccepterId=%s
            ORDER BY t.CreatedAt DESC
        """, conn, params=(user_srn, user_srn))
        st.dataframe(df_barter if not df_barter.empty else pd.DataFrame({"Message": ["No barter transactions."]}), hide_index=True)

    # ── Tab 3: My lend/borrow
    with tab3:
        st.subheader("Lend/Borrow Transactions")
        df_loans = pd.read_sql("""
            SELECT t.TransactionId, r.Title, lender.Name AS Lender, borrower.Name AS Borrower,
                   l.StartDate, l.EndDate, l.Penalty, t.Status
            FROM LendBorrowTransaction l
            JOIN Transaction t    ON l.TransactionId = t.TransactionId
            JOIN Resource r       ON l.ResourceId = r.ResourceId
            JOIN Student lender   ON l.LenderId = lender.SRN
            JOIN Student borrower ON l.BorrowerId = borrower.SRN
            WHERE l.LenderId=%s OR l.BorrowerId=%s
            ORDER BY t.CreatedAt DESC
        """, conn, params=(user_srn, user_srn))
        st.dataframe(df_loans if not df_loans.empty else pd.DataFrame({"Message": ["No loan transactions."]}), hide_index=True)

    # ── Tab 4: Reviews & Reminders
    with tab4:
        st.subheader("My Reviews")
        df_reviews = pd.read_sql("""
            SELECT rv.ReviewId, r.Title AS Resource, rv.Rating, rv.Comment, DATE(rv.CreatedAt) AS Date
            FROM Review rv JOIN Resource r ON rv.ResourceId = r.ResourceId
            WHERE rv.ReviewerId = %s ORDER BY rv.CreatedAt DESC
        """, conn, params=(user_srn,))
        st.dataframe(df_reviews if not df_reviews.empty else pd.DataFrame({"Message": ["No reviews written yet."]}), hide_index=True)

        st.markdown("---")
        st.subheader("Write a Review")

        # Resources user has completed a transaction for
        eligible = pd.read_sql("""
            SELECT DISTINCT r.ResourceId, r.Title
            FROM Resource r
            JOIN BuySellTransaction b ON r.ResourceId = b.ResourceId
            JOIN Transaction t ON b.TransactionId = t.TransactionId
            WHERE b.BuyerId = %s AND t.Status = 'COMPLETED'
              AND r.ResourceId NOT IN (SELECT ResourceId FROM Review WHERE ReviewerId = %s)
            UNION
            SELECT DISTINCT r.ResourceId, r.Title
            FROM Resource r
            JOIN LendBorrowTransaction l ON r.ResourceId = l.ResourceId
            JOIN Transaction t ON l.TransactionId = t.TransactionId
            WHERE l.BorrowerId = %s AND t.Status = 'COMPLETED'
              AND r.ResourceId NOT IN (SELECT ResourceId FROM Review WHERE ReviewerId = %s)
        """, conn, params=(user_srn, user_srn, user_srn, user_srn))

        if eligible.empty:
            st.info("No completed transactions to review yet.")
        else:
            elig_map = {f"{r['Title']} (#{r['ResourceId']})": r['ResourceId'] for r in eligible.to_dict('records')}
            with st.form("new_review_form"):
                sel_item = st.selectbox("Select Item to Review", list(elig_map.keys()))
                rating   = st.slider("Rating", 1, 5, 5)
                comment  = st.text_area("Comments (optional)")
                if st.form_submit_button("Submit Review", type="primary"):
                    res_id = elig_map[sel_item]
                    try:
                        rc = conn.cursor()
                        rc.execute(
                            "INSERT INTO Review (Rating, Comment, ReviewerId, ResourceId) VALUES (%s,%s,%s,%s)",
                            (rating, comment, user_srn, res_id)
                        )
                        conn.commit(); rc.close()
                        st.success("Review submitted!"); st.rerun()
                    except mysql.connector.Error as err:
                        st.error(f"Failed: {err}")

        st.markdown("---")
        st.subheader("My Reminders")
        df_rem = pd.read_sql(
            "SELECT ReminderId, Message, Status, ReminderDate FROM Reminder WHERE StudentId=%s ORDER BY ReminderDate DESC",
            conn, params=(user_srn,)
        )
        st.dataframe(df_rem if not df_rem.empty else pd.DataFrame({"Message": ["No reminders."]}), hide_index=True)

    conn.close()

# ─── 9. Admin Dashboard ───────────────────────────────────────────────────────
def page_admin():
    render_sidebar(is_admin=True)
    st.title("Admin Dashboard")

    conn = get_db_connection()
    if not conn: return

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    def stat(conn, sql):
        c = conn.cursor(); c.execute(sql); r = c.fetchone(); c.close()
        return r[0] if r else 0

    col1.metric("Students",     stat(conn, "SELECT COUNT(*) FROM Student"))
    col2.metric("Resources",    stat(conn, "SELECT COUNT(*) FROM Resource"))
    col3.metric("Transactions", stat(conn, "SELECT COUNT(*) FROM Transaction"))
    col4.metric("Reviews",      stat(conn, "SELECT COUNT(*) FROM Review"))

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Students", "Resources", "All Transactions"])

    with tab1:
        st.subheader("Manage Students")
        df_students = pd.read_sql(
            "SELECT SRN, Name, Email, Dept, Phone, IF(Suspended,'Suspended','Active') AS Status FROM Student",
            conn
        )
        st.dataframe(df_students, hide_index=True)

        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Suspend / Activate")
            with st.form("suspend_form"):
                srn_input = st.text_input("Enter SRN")
                action    = st.radio("Action", ["Suspend", "Activate"])
                if st.form_submit_button("Apply", type="primary"):
                    if srn_input:
                        try:
                            c = conn.cursor()
                            c.execute(
                                "UPDATE Student SET Suspended=%s WHERE SRN=%s",
                                (action == "Suspend", srn_input)
                            )
                            conn.commit(); c.close()
                            st.success(f"Student {srn_input} {action.lower()}d."); st.rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Error: {err}")

        with col_b:
            st.subheader("Delete Student")
            with st.form("delete_student_form"):
                del_srn = st.text_input("SRN to Delete")
                if st.form_submit_button("Delete Permanently", type="primary"):
                    if del_srn:
                        try:
                            c = conn.cursor()
                            c.execute("DELETE FROM Student WHERE SRN=%s", (del_srn,))
                            conn.commit(); c.close()
                            st.success(f"Student {del_srn} deleted."); st.rerun()
                        except mysql.connector.Error as err:
                            st.error(f"Error: {err}")

    with tab2:
        st.subheader("All Resources")
        df_all_res = pd.read_sql("""
            SELECT r.ResourceId, r.Title, s.Name AS Owner, r.ListingType,
                   r.Status, CONCAT(c.MainType,' / ',c.SubType) AS Category
            FROM Resource r
            JOIN Student s  ON r.OwnerId = s.SRN
            JOIN Category c ON r.CategoryId = c.CategoryId
        """, conn)
        st.dataframe(df_all_res, hide_index=True)

        with st.form("admin_del_res_form"):
            del_res_id = st.number_input("Resource ID to Remove", min_value=1, step=1)
            if st.form_submit_button("Remove Resource", type="primary"):
                try:
                    c = conn.cursor()
                    c.execute("DELETE FROM Resource WHERE ResourceId=%s", (int(del_res_id),))
                    conn.commit(); c.close()
                    st.success(f"Resource #{del_res_id} removed."); st.rerun()
                except mysql.connector.Error as err:
                    st.error(f"Error: {err}")

    with tab3:
        st.subheader("All Transactions")
        df_txns = pd.read_sql(
            "SELECT TransactionId, TransactionType, Status, DATE(CreatedAt) AS Date FROM Transaction ORDER BY CreatedAt DESC",
            conn
        )
        st.dataframe(df_txns if not df_txns.empty else pd.DataFrame({"Message": ["No transactions yet."]}), hide_index=True)

    conn.close()

# ─── Main Router ──────────────────────────────────────────────────────────────
srn = st.session_state.logged_in_srn

if srn is None:
    p = st.session_state.page
    if p == 'login':  page_login()
    elif p == 'signup': page_signup()
    else: page_landing()

elif srn.startswith("ADMIN::"):
    page_admin()

else:
    p = st.session_state.page
    if p == 'home':          page_home_browse()
    elif p == 'upload_sell':   page_upload_item('sell')
    elif p == 'upload_lend':   page_upload_item('lend')
    elif p == 'upload_barter': page_upload_item('barter')
    elif p == 'buysell':       page_buysell()
    elif p == 'lendborrow':    page_lendborrow()
    elif p == 'barter':        page_barter()
    elif p == 'my_activity':   page_my_activity()
    else: page_home_browse()