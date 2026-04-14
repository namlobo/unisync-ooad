package controller;

import model.user.Student;
import service.StudentService;

import java.util.List;

public class StudentController {

    private final StudentService studentService;

    public StudentController() {
        this.studentService = new StudentService();
    }

    public void registerStudent(Student student) {
        studentService.registerStudent(student);
        System.out.println("[INFO] Student registered successfully.");
    }

    public Student loginStudent(String email, String password) {
        Student student = studentService.login(email, password);
        System.out.println("[INFO] Login successful.");
        return student;
    }

    public List<Student> getAllStudents() {
        return studentService.getAllStudents();
    }

    public void updateStudent(Student student) {
        studentService.updateStudent(student);
        System.out.println("[INFO] Student updated.");
    }

    public void deleteStudent(String studentId) {
        studentService.removeStudent(studentId);
        System.out.println("[INFO] Student deleted.");
    }
}