package dao.impl;

import dao.DBConnection;
import dao.interfaces.StudentDAO;
import model.user.Student;

import java.sql.*;
import java.util.*;

public class StudentDAOImpl implements StudentDAO {

    @Override
    public void save(Student student) {
        String sql = "INSERT INTO Student (SRN, Name, Email, Phone, Password, Dept, Suspended) VALUES (?, ?, ?, ?, ?, ?, ?)";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, student.getId());
            ps.setString(2, student.getName());
            ps.setString(3, student.getEmail());
            ps.setString(4, student.getPhone());
            ps.setString(5, student.getPassword()); 
            ps.setString(6, student.getDepartment());
            ps.setBoolean(7, false); // default

            ps.executeUpdate();

            System.out.println("Student registered successfully!");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public Optional<Student> findById(String id) {
        String sql = "SELECT * FROM Student WHERE SRN = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, id);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                return Optional.of(mapStudent(rs));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return Optional.empty();
    }

    @Override
    public Optional<Student> findByEmail(String email) {
        String sql = "SELECT * FROM Student WHERE Email = ?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, email);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                return Optional.of(mapStudent(rs));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return Optional.empty();
    }

    @Override
    public List<Student> findAll() {
        List<Student> students = new ArrayList<>();
        String sql = "SELECT * FROM Student";

        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement()) {

            ResultSet rs = stmt.executeQuery(sql);

            while (rs.next()) {
                students.add(mapStudent(rs));
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }

        return students;
    }

    @Override
    public void update(Student student) {
        String sql = "UPDATE Student SET Name=?, Email=?, Phone=?, Dept=? WHERE SRN=?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, student.getName());
            ps.setString(2, student.getEmail());
            ps.setString(3, student.getPhone());
            ps.setString(4, student.getDepartment());
            ps.setString(5, student.getId());

            ps.executeUpdate();

            System.out.println("Student updated!");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void delete(String id) {
        String sql = "DELETE FROM Student WHERE SRN=?";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, id);
            ps.executeUpdate();

            System.out.println("Student deleted!");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private Student mapStudent(ResultSet rs) throws SQLException {
        return new Student(
                rs.getString("SRN"),
                rs.getString("Name"),
                rs.getString("Email"),
                rs.getString("Phone"),
                rs.getString("Password"),
                rs.getString("Dept")
        );
    }
}