package dao.interfaces;

import model.transaction.Transaction;
import java.util.List;

public interface TransactionDAO {

    void save(Transaction transaction);

    List<Transaction> findAll();

    void updateStatus(int transactionId, String status);
}