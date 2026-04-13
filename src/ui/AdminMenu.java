package ui;

import controller.AdminController;
import controller.StudentController;
import model.user.Admin;
import model.user.Student;

import java.util.Scanner;

public class AdminMenu {

    private final Scanner scanner;
    private final AdminController adminController;
    private final StudentController studentController;
    private Admin admin;

    public AdminMenu() {
        scanner = new Scanner(System.in);
        adminController = new AdminController();
        studentController = new StudentController();
    }

    public void show() {
        loginAdmin();

        if (admin == null) {
            return;
        }

        while (true) {
            System.out.println("\n===== Admin Portal =====");
            System.out.println("1. View All Students");
            System.out.println("2. Suspend Student");
            System.out.println("3. Activate Student");
            System.out.println("4. View System Statistics");
            System.out.println("5. Logout");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    viewAllStudents();
                    break;

                case 2:
                    suspendStudent();
                    break;

                case 3:
                    activateStudent();
                    break;

                case 4:
                    viewStatistics();
                    break;

                case 5:
                    System.out.println("Admin logged out successfully.");
                    return;

                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    private void loginAdmin() {
        System.out.print("Admin Email: ");
        String email = scanner.nextLine();

        System.out.print("Password: ");
        String password = scanner.nextLine();

        // In a real system, validate admin credentials against database
        if (email.equals("admin@unisync.com") && password.equals("admin123")) {
            admin = new Admin("ADMIN001", "Administrator", email, "+1234567890", password);
            System.out.println("[INFO] Admin login successful.");
        } else {
            System.out.println("[ERROR] Invalid admin credentials.");
        }
    }

    private void viewAllStudents() {
        System.out.println("\n===== All Students =====");
        java.util.List<Student> students = studentController.getAllStudents();

        if (students.isEmpty()) {
            System.out.println("No students registered.");
        } else {
            for (Student student : students) {
                String status = student.isSuspended() ? "[SUSPENDED]" : "[ACTIVE]";
                System.out.println(status + " " + student.getName() + " (" + student.getEmail() + ")");
            }
        }
    }

    private void suspendStudent() {
        System.out.print("Enter Student Email: ");
        String email = scanner.nextLine();

        java.util.List<Student> students = studentController.getAllStudents();

        for (Student student : students) {
            if (student.getEmail().equals(email)) {
                adminController.suspendStudent(admin, student);
                return;
            }
        }

        System.out.println("[ERROR] Student not found.");
    }

    private void activateStudent() {
        System.out.print("Enter Student Email: ");
        String email = scanner.nextLine();

        java.util.List<Student> students = studentController.getAllStudents();

        for (Student student : students) {
            if (student.getEmail().equals(email)) {
                adminController.activateStudent(admin, student);
                return;
            }
        }

        System.out.println("[ERROR] Student not found.");
    }

    private void viewStatistics() {
        System.out.println("\n===== System Statistics =====");
        System.out.println("Total Registered Students: " + studentController.getAllStudents().size());
        System.out.println("Total Resources Listed: [To be implemented]");
        System.out.println("Total Transactions: [To be implemented]");
        System.out.println("Platform Status: ACTIVE");
    }
}