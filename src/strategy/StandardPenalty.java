package strategy;

public class StandardPenalty implements PenaltyStrategy {

    @Override
    public double calculatePenalty(int daysLate) {
        return daysLate * 10.0;
    }
}