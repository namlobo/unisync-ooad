package model.reminder;

import java.time.LocalDate;

public class Reminder {

    private int reminderId;
    private String message;
    private String status;
    private LocalDate reminderDate;

    public Reminder(int reminderId, String message, String status, LocalDate reminderDate) {
        this.reminderId = reminderId;
        this.message = message;
        this.status = status;
        this.reminderDate = reminderDate;
    }

    public int getReminderId() {
        return reminderId;
    }

    public String getMessage() {
        return message;
    }

    public String getStatus() {
        return status;
    }

    public LocalDate getReminderDate() {
        return reminderDate;
    }

    public void markRead() {
        status = "READ";
    }
}