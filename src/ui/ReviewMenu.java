package ui;

import controller.ReviewController;
import model.review.Review;
import model.user.Student;

import java.util.Scanner;

public class ReviewMenu {

    private final Scanner scanner;
    private final ReviewController reviewController;
    private Student reviewer;

    public ReviewMenu() {
        scanner = new Scanner(System.in);
        reviewController = new ReviewController();
    }

    public ReviewMenu(Student reviewer) {
        scanner = new Scanner(System.in);
        reviewController = new ReviewController();
        this.reviewer = reviewer;
    }

    public void show() {

        while (true) {
            System.out.println("\n===== Review Menu =====");
            System.out.println("1. Submit Review");
            System.out.println("2. View Reviews for Resource");
            System.out.println("3. Back");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {

                case 1:
                    submitReview();
                    break;

                case 2:
                    viewResourceReviews();
                    break;

                case 3:
                    return;

                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    private void submitReview() {
        System.out.println("\n===== Submit Review =====");

        System.out.print("Resource ID: ");
        int resourceId = scanner.nextInt();
        scanner.nextLine();

        System.out.print("Rating (1-5): ");
        int rating = scanner.nextInt();
        scanner.nextLine();

        if (rating < 1 || rating > 5) {
            System.out.println("[ERROR] Rating must be between 1 and 5.");
            return;
        }

        System.out.print("Comment: ");
        String comment = scanner.nextLine();

        if (reviewer == null) {
            System.out.println("[ERROR] Please login first.");
            return;
        }

        Review review = new Review(resourceId, rating, comment, reviewer, null);

        reviewController.submitReview(review);
    }

    private void viewResourceReviews() {
        System.out.println("\n===== View Reviews =====");

        System.out.print("Resource ID: ");
        int resourceId = scanner.nextInt();
        scanner.nextLine();

        java.util.List<Review> reviews = reviewController.getReviewsForResource(resourceId);

        if (reviews.isEmpty()) {
            System.out.println("No reviews found for this resource.");
        } else {
            for (Review review : reviews) {
                System.out.println("Rating: " + review.getRating() + " - " + review.getComment());
            }
        }
    }
}