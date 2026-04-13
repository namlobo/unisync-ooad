package ui;

import controller.TransactionController;
import model.resource.Resource;
import model.transaction.Transaction;
import model.user.Student;

import java.util.Scanner;

public class TransactionMenu {

    private final Scanner scanner;
    private final TransactionController transactionController;
    private final Student student;

    public TransactionMenu(Student student) {
        scanner = new Scanner(System.in);
        transactionController = new TransactionController();
        this.student = student;
    }

    public void show() {

        while (true) {
            System.out.println("\n===== Transaction Menu =====");
            System.out.println("1. Create Buy/Sell Transaction");
            System.out.println("2. Create Lend/Borrow Transaction");
            System.out.println("3. Create Barter Transaction");
            System.out.println("4. View My Transactions");
            System.out.println("5. Back");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {

                case 1:
                    createBuySellTransaction();
                    break;

                case 2:
                    createLendBorrowTransaction();
                    break;

                case 3:
                    createBarterTransaction();
                    break;

                case 4:
                    viewMyTransactions();
                    break;

                case 5:
                    return;

                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    private void createBuySellTransaction() {
        System.out.println("\n===== Buy/Sell Transaction =====");

        System.out.print("Resource ID: ");
        int resourceId = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Are you the Seller? (y/n): ");
        String role = scanner.nextLine();

        System.out.print("Price: ");
        double price = scanner.nextDouble();
        scanner.nextLine();

        // Get resource from controller
        Resource resource = transactionController.getResource(resourceId);

        if (resource == null) {
            System.out.println("[ERROR] Resource not found.");
            return;
        }

        Student seller = "y".equalsIgnoreCase(role) ? student : new Student("temp", "Other Student", "temp@email.com", "1234567890", "pass", "CSE");
        Student buyer = "y".equalsIgnoreCase(role) ? new Student("temp", "Other Student", "temp@email.com", "1234567890", "pass", "CSE") : student;

        Transaction transaction = transactionController.createBuySell(resource, seller, buyer, price);

        System.out.println("[SUCCESS] Transaction created.");
        System.out.println("Transaction ID: " + transaction.getTransactionId());
    }

    private void createLendBorrowTransaction() {
        System.out.println("\n===== Lend/Borrow Transaction =====");

        System.out.print("Resource ID: ");
        int resourceId = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Borrow Duration (days): ");
        int duration = scanner.nextInt();
        scanner.nextLine();

        Resource resource = transactionController.getResource(resourceId);

        if (resource == null) {
            System.out.println("[ERROR] Resource not found.");
            return;
        }

        System.out.println("[SUCCESS] Lend/Borrow transaction initiated.");
        System.out.println("Duration: " + duration + " days");
    }

    private void createBarterTransaction() {
        System.out.println("\n===== Barter Transaction =====");

        System.out.print("Your Resource ID (offering): ");
        int offeredResourceId = scanner.nextInt();

        System.out.print("Requested Resource ID: ");
        int requestedResourceId = scanner.nextInt();
        scanner.nextLine();

        System.out.println("[SUCCESS] Barter transaction initiated.");
        System.out.println("Waiting for other student to accept the trade...");
    }

    private void viewMyTransactions() {
        System.out.println("\n===== My Transactions =====");

        java.util.List<Transaction> transactions = transactionController.getAllTransactions();

        if (transactions.isEmpty()) {
            System.out.println("No transactions found.");
        } else {
            for (Transaction transaction : transactions) {
                System.out.println("Transaction ID: " + transaction.getTransactionId() + " - Status: " + transaction.getStatus());
            }
        }
    }
}