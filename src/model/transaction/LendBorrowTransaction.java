package model.transaction;

import java.time.LocalDate;
import model.resource.Resource;
import model.user.Student;

public class LendBorrowTransaction extends Transaction {

    private Resource resource;
    private Student lender;
    private Student borrower;
    private LocalDate startDate;
    private LocalDate endDate;
    private double penalty;

    public LendBorrowTransaction(int transactionId,
                                 Resource resource,
                                 Student lender,
                                 Student borrower,
                                 LocalDate startDate,
                                 LocalDate endDate) {
        super(transactionId);
        this.resource = resource;
        this.lender = lender;
        this.borrower = borrower;
        this.startDate = startDate;
        this.endDate = endDate;
    }

    @Override
    public void initiate() {
        resource.markBorrowed();
        status = TransactionStatus.PENDING;
    }

    @Override
    public void complete() {
        resource.makeAvailable();
        status = TransactionStatus.COMPLETED;
    }

    @Override
    public void cancel() {
        status = TransactionStatus.CANCELLED;
    }

    public void setPenalty(double penalty) {
        this.penalty = penalty;
    }
}