import dao.DBConnection;
import java.sql.Connection;

public class TestDB {
    public static void main(String[] args) {
        try {
            Connection conn = DBConnection.getConnection();

            if (conn != null) {
                System.out.println("✅ Database connected successfully!");
            } else {
                System.out.println("❌ Connection failed!");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}