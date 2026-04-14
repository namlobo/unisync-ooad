package singleton;

import model.user.Student;

public class SessionManager {

    private static SessionManager instance;
    private Student currentStudent;

    private SessionManager() {
    }

    public static SessionManager getInstance() {
        if (instance == null) {
            instance = new SessionManager();
        }
        return instance;
    }

    public void login(Student student) {
        this.currentStudent = student;
    }

    public void logout() {
        this.currentStudent = null;
    }

    public Student getCurrentStudent() {
        return currentStudent;
    }

    public boolean isLoggedIn() {
        return currentStudent != null;
    }
}