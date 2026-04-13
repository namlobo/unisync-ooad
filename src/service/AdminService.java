package service;

import model.user.Admin;
import model.user.Student;

public class AdminService {

    public void suspendStudent(Admin admin, Student student) {
        admin.suspendStudent(student);
    }

    public void activateStudent(Admin admin, Student student) {
        admin.activateStudent(student);
    }
}