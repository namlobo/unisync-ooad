package strategy;

public class PremiumPenalty implements PenaltyStrategy {

    @Override
    public double calculatePenalty(int daysLate) {
        return daysLate * 5.0;
    }
}