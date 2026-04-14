package dao.impl;

import dao.DBConnection;
import dao.interfaces.TransactionDAO;
import model.transaction.Transaction;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TransactionDAOImpl implements TransactionDAO {

    @Override
    public void save(Transaction transaction) {
        String sql = "INSERT INTO Transaction (TransactionId, Status, CreatedAt) VALUES (?, ?, ?)";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, transaction.getTransactionId());
            ps.setString(2, transaction.getStatus().name());
            ps.setTimestamp(3, Timestamp.valueOf(java.time.LocalDateTime.now()));

            ps.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public List<Transaction> findAll() {
        List<Transaction> transactions = new ArrayList<>();
        String sql = "SELECT TransactionId, Status, CreatedAt FROM Transaction";

        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement()) {

            ResultSet rs = stmt.executeQuery(sql);

            while (rs.next()) {
                // Return basic transaction info
                // Full implementation would reconstruct specific transaction types
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return transactions;
    }

    @Override
    public void updateStatus(int transactionId, String status) {
        String sql = "UPDATE Transaction SET Status = ? WHERE TransactionId = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, status);
            ps.setInt(2, transactionId);

            ps.executeUpdate();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}