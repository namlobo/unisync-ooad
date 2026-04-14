package service;

import model.reminder.Reminder;
import observer.ReminderObserver;
import observer.ReminderSubject;
import observer.StudentNotification;
import model.user.Student;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class ReminderService {

    private final ReminderSubject reminderSubject;
    private final List<Reminder> reminders;
    private int reminderCounter = 0;

    public ReminderService() {
        this.reminderSubject = new ReminderSubject();
        this.reminders = new ArrayList<>();
    }

    public void registerObserver(ReminderObserver observer) {
        reminderSubject.addObserver(observer);
    }

    public void registerStudentObserver(Student student) {
        ReminderObserver observer = new StudentNotification(student.getName());
        reminderSubject.addObserver(observer);
    }

    public void removeObserver(ReminderObserver observer) {
        reminderSubject.removeObserver(observer);
    }

    public Reminder generateReminder(String message) {

        Reminder reminder = new Reminder(
                ++reminderCounter,
                message,
                "UNREAD",
                LocalDate.now()
        );

        reminders.add(reminder);
        reminderSubject.notifyObservers(message);

        return reminder;
    }

    public void sendLendBorrowReminder(String borrowerName, String resourceTitle, LocalDate dueDate) {
        String message = "[BORROW REMINDER] " + borrowerName + " has borrowed " + resourceTitle + " due on " + dueDate;
        generateReminder(message);
    }

    public void sendDueReminderForBorrow(String resourceTitle) {
        String message = "[DUE REMINDER] Return " + resourceTitle + " - due soon!";
        generateReminder(message);
    }

    public void sendLateLendReminder(String borrowerName, String resourceTitle, int daysLate) {
        String message = "[LATE ALERT] " + borrowerName + " is " + daysLate + " days late returning " + resourceTitle;
        generateReminder(message);
    }

    public void sendTransactionReminder(String transactionType, String details) {
        String message = "[TRANSACTION] " + transactionType + ": " + details;
        generateReminder(message);
    }

    public List<Reminder> getAllReminders() {
        return new ArrayList<>(reminders);
    }

    public List<Reminder> getUnreadReminders() {
        List<Reminder> unread = new ArrayList<>();
        for (Reminder reminder : reminders) {
            if ("UNREAD".equals(reminder.getStatus())) {
                unread.add(reminder);
            }
        }
        return unread;
    }

    public void markReminderAsRead(int reminderId) {
        for (Reminder reminder : reminders) {
            if (reminder.getReminderId() == reminderId) {
                reminder.markRead();
                break;
            }
        }
    }
}