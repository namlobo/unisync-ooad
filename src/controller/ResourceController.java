package controller;

import model.resource.Resource;
import service.ResourceService;

import java.util.List;

public class ResourceController {

    private final ResourceService resourceService;

    public ResourceController() {
        this.resourceService = new ResourceService();
    }

    public void addResource(Resource resource) {
        resourceService.addResource(resource);
        System.out.println("[INFO] Resource added successfully.");
    }

    public Resource getResource(int id) {
        return resourceService.getResourceById(id);
    }

    public List<Resource> getAvailableResources() {
        return resourceService.getAvailableResources();
    }

    public void removeResource(int id) {
        resourceService.removeResource(id);
        System.out.println("[INFO] Resource removed.");
    }

    public void markSold(Resource resource) {
        resourceService.markAsSold(resource);
    }

    public void markBorrowed(Resource resource) {
        resourceService.markAsBorrowed(resource);
    }
}