package controller;

import model.user.Admin;
import model.user.Student;
import service.AdminService;

public class AdminController {

    private final AdminService adminService;

    public AdminController() {
        this.adminService = new AdminService();
    }

    public void suspendStudent(Admin admin, Student student) {
        adminService.suspendStudent(admin, student);
        System.out.println("[INFO] Student suspended.");
    }

    public void activateStudent(Admin admin, Student student) {
        adminService.activateStudent(admin, student);
        System.out.println("[INFO] Student activated.");
    }
}