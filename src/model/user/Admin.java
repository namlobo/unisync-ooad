package model.user;

public class Admin extends User {

    public Admin(String id, String name, String email, String phone, String password) {
        super(id, name, email, phone, password);
    }

    @Override
    public boolean login(String password) {
        return this.password.equals(password);
    }

    @Override
    public void logout() {
        System.out.println("Admin logged out successfully.");
    }

    public void suspendStudent(Student student) {
        student.suspend();
    }

    public void activateStudent(Student student) {
        student.activate();
    }
}