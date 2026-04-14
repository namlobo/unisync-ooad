# UniSync — Student Resource Exchange Platform

> A full-stack student marketplace for buying, selling, lending, borrowing, and bartering academic resources. Built with Java (OOAD patterns) + Streamlit (Python UI) + MySQL.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Team & Responsibilities](#team--responsibilities)
- [Architecture](#architecture)
- [OOAD Design Patterns](#ooad-design-patterns)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup & Running](#setup--running)
- [API Endpoints](#api-endpoints)
- [Deliverables](#deliverables)

---

## Project Overview

UniSync is a campus-level peer-to-peer resource sharing platform. Students can:

- **Sell / Buy** textbooks, electronics, and equipment
- **Lend / Borrow** items with due-date tracking and late penalties
- **Barter** items directly with other students
- **Review** resources they have transacted with
- **Receive reminders** for upcoming return deadlines

Administrators can manage students (suspend/activate/delete), remove inappropriate listings, and view platform-wide transaction statistics.

---

## Team & Responsibilities

| Member | Modules | Classes |
|--------|---------|---------|
| **Meenakshi** | Review, Student, Resource | `Review`, `Student`, `User`, `Resource`, `ResourceStatus`, `ListingType`, `ReviewDAO`, `StudentDAO`, `ResourceDAO` + impls, `ReviewService`, `StudentService`, `ResourceService`, `ReviewMenu`, `StudentMenu`, `ResourceMenu` |
| **Nam** | Category, Transaction, Reminder + UI | `Category`, `Transaction`, `TransactionStatus`, `BarterTransaction`, `Reminder`, `TransactionFactory`, `TransactionDAO` + impl, `TransactionService`, `ReminderService`, `ReminderObserver`, `ReminderSubject`, `StudentNotification`, `SessionManager`|
| **Neema** | BuySell, LendBorrow, Strategy, Admin | `BuySellTransaction`, `LendBorrowTransaction`, `PenaltyStrategy`, `StandardPenalty`, `PremiumPenalty`, `Admin`, `AdminService`, `AdminController`, `TransactionController`, `AdminMenu`, `TransactionMenu`, `MainMenu` |


## Database Schema

Key tables and relationships:

| Table | Description |
|-------|-------------|
| `Student` | Registered students (SRN, Name, Email, Dept, Suspended) |
| `Admin` | Admin accounts |
| `Category` | Resource categories (MainType / SubType) |
| `Resource` | Listed items with Status and ListingType (SELL/LEND/BARTER) |
| `Transaction` | Base transaction record (type + status) |
| `BuySellTransaction` | Extends Transaction — Price, Seller, Buyer |
| `LendBorrowTransaction` | Extends Transaction — Dates, Penalty |
| `BarterTransaction` | Extends Transaction — OfferedResource, RequestedResource |
| `Review` | 1–5 star ratings on completed transactions |
| `Reminder` | Due-date notifications linked to students + transactions |


## Setup & Running

### Prerequisites

- Java 17+
- Python 3.9+
- MySQL 8.0+
- `pip install streamlit mysql-connector-python pandas requests`

### 1. Database Setup (everyone does this once)

```bash
mysql -u root -p
CREATE DATABASE unisync;
USE unisync;
SOURCE /path/to/UNISYNC.sql;
```

### 2. Configure DB credentials

Each member creates this file locally — **never commit it**:

```
# src/config/db.properties
db.url=jdbc:mysql://localhost:3306/unisync
db.username=root
db.password=YOUR_PASSWORD
db.driver=com.mysql.cj.jdbc.Driver
```

### 3. Compile the Java backend

```bash
cd ooad_proj

# List all source files
find src -name "*.java" > sources.txt

# Compile
javac -cp "mysql-connector-j-9.6.0.jar:json-20240303.jar" \
      -d out \
      @sources.txt

# On Windows use semicolons:
# javac -cp "mysql-connector-j-9.6.0.jar;json-20240303.jar" -d out @sources.txt
```

### 4. Start the Java API server

```bash
java -cp "out:mysql-connector-j-9.6.0.jar:json-20240303.jar" api.ApiServer
# Windows: java -cp "out;mysql-connector-j-9.6.0.jar;json-20240303.jar" api.ApiServer
```

You should see: `UniSync API running on http://localhost:8080`

### 5. Start the Streamlit UI (new terminal)

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.
---

## API Endpoints

All endpoints served on `http://localhost:8080`.

| Method | Endpoint | Handler | Description |
|--------|----------|---------|-------------|
| POST | `/api/login` | `LoginHandler` | Authenticate student or admin |
| POST | `/api/signup` | `SignupHandler` | Register a new student |
| GET | `/api/resources` | `GetResourcesHandler` | List available resources |
| POST | `/api/resource` | `ResourceHandler` | Add a new resource listing |
| GET | `/api/transactions` | `TransactionsHandler` | Get transactions for a student |
| POST | `/api/borrow` | `BorrowHandler` | Initiate a lend/borrow transaction |
| POST | `/api/return` | `ReturnHandler` | Complete a return (calculates penalty) |

