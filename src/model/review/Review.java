package model.review;

import model.resource.Resource;
import model.user.Student;

public class Review {

    private int reviewId;
    private int rating;
    private String comment;
    private Student reviewer;
    private Resource resource;

    public Review(int reviewId, int rating, String comment, Student reviewer, Resource resource) {
        this.reviewId = reviewId;
        this.rating = rating;
        this.comment = comment;
        this.reviewer = reviewer;
        this.resource = resource;
    }

    public int getRating() {
        return rating;
    }

    public String getComment() {
        return comment;
    }
    public org.json.JSONObject toJson() {
        org.json.JSONObject json = new org.json.JSONObject();
        json.put("reviewId", reviewId);
        json.put("rating", rating);
        json.put("comment", comment);
        json.put("reviewer", reviewer != null ? reviewer.toJson() : org.json.JSONObject.NULL);
        json.put("resourceId", resource != null ? resource.getResourceId() : -1);
        return json;
    }
}