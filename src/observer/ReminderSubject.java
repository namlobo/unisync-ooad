package observer;

import java.util.ArrayList;
import java.util.List;

public class ReminderSubject {

    private final List<ReminderObserver> observers;

    public ReminderSubject() {
        observers = new ArrayList<>();
    }

    public void addObserver(ReminderObserver observer) {
        observers.add(observer);
    }

    public void removeObserver(ReminderObserver observer) {
        observers.remove(observer);
    }

    public void notifyObservers(String message) {
        for (ReminderObserver observer : observers) {
            observer.update(message);
        }
    }
}