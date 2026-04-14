package model.transaction;

import model.resource.Resource;
import model.user.Student;

public class BarterTransaction extends Transaction {

    private Resource offeredResource;
    private Resource requestedResource;
    private Student proposer;
    private Student accepter;

    public BarterTransaction(int transactionId,
                             Resource offeredResource,
                             Resource requestedResource,
                             Student proposer,
                             Student accepter) {
        super(transactionId);
        this.offeredResource = offeredResource;
        this.requestedResource = requestedResource;
        this.proposer = proposer;
        this.accepter = accepter;
    }

    @Override
    public void initiate() {
        status = TransactionStatus.PENDING;
    }

    @Override
    public void complete() {
        status = TransactionStatus.COMPLETED;
    }

    @Override
    public void cancel() {
        status = TransactionStatus.CANCELLED;
    }
}