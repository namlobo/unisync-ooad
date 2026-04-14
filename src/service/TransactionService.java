package service;

import dao.interfaces.TransactionDAO;
import dao.impl.TransactionDAOImpl;

import factory.TransactionFactory;

import model.resource.Resource;
import model.transaction.Transaction;
import model.user.Student;

import java.util.List;

public class TransactionService {

    private final TransactionDAO transactionDAO;
    private final ResourceService resourceService;

    public TransactionService() {
        this.transactionDAO = new TransactionDAOImpl();
        this.resourceService = new ResourceService();
    }

    // 🔥 LEND / BORROW TRANSACTION
    public Transaction createLendBorrowTransaction(int resourceId,
                                                   String lenderId,
                                                   String borrowerId,
                                                   String startDate,
                                                   String endDate) {

        Resource resource = resourceService.getResourceById(resourceId);

        Student lender = new Student(lenderId, "", "", "", "", "");
        Student borrower = new Student(borrowerId, "", "", "", "", "");

        Transaction transaction = TransactionFactory.createTransaction(
                "LENDBORROW",
                resource,
                lender,
                borrower,
                0.0
        );

        transaction.initiate();

        transactionDAO.save(transaction);

        return transaction;
    }

    // 🔥 BUY / SELL TRANSACTION
    public Transaction createBuySellTransaction(Resource resource,
                                                Student seller,
                                                Student buyer,
                                                double price) {

        Transaction transaction = TransactionFactory.createTransaction(
                "BUYSELL",
                resource,
                seller,
                buyer,
                price
        );

        transaction.initiate();

        transactionDAO.save(transaction);

        return transaction;
    }

    // 🔥 COMPLETE TRANSACTION (GENERIC)
    public void completeTransaction(Transaction transaction) {

        transaction.complete();

        // Only update transaction status if DAO supports it
        try {
            transactionDAO.updateStatus(
                    transaction.getTransactionId(),
                    transaction.getStatus().name()
            );
        } catch (Exception ignored) {
            // Safe fallback if method not implemented
        }
    }

    // 🔥 RETURN BORROWED ITEM
    public void completeLendBorrowTransaction(int transactionId) {

        try {
            transactionDAO.updateStatus(transactionId, "COMPLETED");
        } catch (Exception ignored) {
            // fallback if DAO method not present
        }
    }

    // 🔥 GET ALL TRANSACTIONS
    public List<Transaction> getAllTransactions() {
        return transactionDAO.findAll();
    }
}