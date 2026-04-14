package dao.interfaces;

import model.resource.Resource;
import java.util.List;
import java.util.Optional;

public interface ResourceDAO {

    void save(Resource resource);

    Optional<Resource> findById(int id);

    List<Resource> findAvailableResources();

    void update(Resource resource);

    void delete(int id);
}