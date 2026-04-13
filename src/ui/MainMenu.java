package ui;

import java.util.Scanner;

public class MainMenu {

    private final Scanner scanner;

    public MainMenu() {
        scanner = new Scanner(System.in);
    }

    public void launch() {

        while (true) {
            System.out.println("\n===== UniSync Main Menu =====");
            System.out.println("1. Student Portal");
            System.out.println("2. Admin Portal");
            System.out.println("3. Exit");
            System.out.print("Choose option: ");

            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    new StudentMenu().show();
                    break;

                case 2:
                    new AdminMenu().show();
                    break;

                case 3:
                    System.out.println("Exiting UniSync...");
                    return;

                default:
                    System.out.println("Invalid choice.");
            }
        }
    }

    public static void main(String[] args) {
        new MainMenu().launch();
    }
}