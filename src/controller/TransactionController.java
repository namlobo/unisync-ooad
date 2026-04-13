package controller;

import model.resource.Resource;
import model.transaction.Transaction;
import model.user.Student;
import service.TransactionService;
import service.ResourceService;

import java.util.List;

public class TransactionController {

    private final TransactionService transactionService;
    private final ResourceService resourceService;

    public TransactionController() {
        this.transactionService = new TransactionService();
        this.resourceService = new ResourceService();
    }

    public Transaction createBuySell(Resource resource,
                                     Student seller,
                                     Student buyer,
                                     double price) {

        Transaction transaction = transactionService.createBuySellTransaction(
                resource,
                seller,
                buyer,
                price
        );

        System.out.println("[INFO] Transaction initiated.");
        return transaction;
    }

    public void completeTransaction(Transaction transaction, Resource resource) {
        transactionService.completeTransaction(transaction);
        System.out.println("[INFO] Transaction completed.");
    }

    public List<Transaction> getAllTransactions() {
        return transactionService.getAllTransactions();
    }

    public Resource getResource(int resourceId) {
        try {
            return resourceService.getResourceById(resourceId);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }
}