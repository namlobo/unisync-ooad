package dao.interfaces;

import model.review.Review;
import java.util.List;

public interface ReviewDAO {

    void save(Review review);

    List<Review> findByResource(int resourceId);
}