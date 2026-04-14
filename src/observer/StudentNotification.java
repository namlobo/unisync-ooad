package observer;

public class StudentNotification implements ReminderObserver {

    private final String studentName;

    public StudentNotification(String studentName) {
        this.studentName = studentName;
    }

    @Override
    public void update(String message) {
        System.out.println("[NOTIFICATION] " + studentName + ": " + message);
    }
}