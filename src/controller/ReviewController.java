package controller;

import model.review.Review;
import service.ReviewService;

import java.util.List;

public class ReviewController {

    private final ReviewService reviewService;

    public ReviewController() {
        this.reviewService = new ReviewService();
    }

    public void submitReview(Review review) {
        reviewService.submitReview(review);
        System.out.println("[INFO] Review submitted.");
    }

    public List<Review> getReviewsForResource(int resourceId) {
        return reviewService.getReviewsForResource(resourceId);
    }
}