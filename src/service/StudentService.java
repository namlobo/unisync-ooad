package service;

import dao.interfaces.StudentDAO;
import dao.impl.StudentDAOImpl;
import model.user.Student;

import java.util.List;
import java.util.Optional;

public class StudentService {

    private final StudentDAO studentDAO;

    public StudentService() {
        this.studentDAO = new StudentDAOImpl();
    }

    public void registerStudent(Student student) {

        Optional<Student> existing = studentDAO.findByEmail(student.getEmail());

        if (existing.isPresent()) {
            throw new IllegalArgumentException("Student already registered with this email.");
        }

        studentDAO.save(student);
    }

    public Student login(String email, String password) {

        Optional<Student> studentOptional = studentDAO.findByEmail(email);

        if (studentOptional.isEmpty()) {
            throw new IllegalArgumentException("Student not found.");
        }

        Student student = studentOptional.get();

        if (!student.login(password)) {
            throw new IllegalArgumentException("Invalid password.");
        }

        return student;
    }

    public List<Student> getAllStudents() {
        return studentDAO.findAll();
    }

    public void updateStudent(Student student) {
        studentDAO.update(student);
    }

    public void removeStudent(String studentId) {
        studentDAO.delete(studentId);
    }
}