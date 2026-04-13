package model.transaction;

import model.resource.Resource;
import model.user.Student;

public class BuySellTransaction extends Transaction {

    private Resource resource;
    private Student seller;
    private Student buyer;
    private double price;

    public BuySellTransaction(int transactionId,
                              Resource resource,
                              Student seller,
                              Student buyer,
                              double price) {
        super(transactionId);
        this.resource = resource;
        this.seller = seller;
        this.buyer = buyer;
        this.price = price;
    }

    @Override
    public void initiate() {
        status = TransactionStatus.PENDING;
    }

    @Override
    public void complete() {
        resource.markSold();
        status = TransactionStatus.COMPLETED;
    }

    @Override
    public void cancel() {
        status = TransactionStatus.CANCELLED;
    }
}