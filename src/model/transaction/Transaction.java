package model.transaction;

import java.time.LocalDateTime;

public abstract class Transaction {

    protected int transactionId;
    protected LocalDateTime createdAt;
    protected TransactionStatus status;

    public Transaction(int transactionId) {
        this.transactionId = transactionId;
        this.createdAt = LocalDateTime.now();
        this.status = TransactionStatus.INITIATED;
    }

    public int getTransactionId() {
        return transactionId;
    }

    public TransactionStatus getStatus() {
        return status;
    }

    public abstract void initiate();

    public abstract void complete();

    public abstract void cancel();
}