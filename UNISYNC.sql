-- UniSync Database Schema
-- MySQL Database Setup Script
-- Created: April 4, 2026

-- Create Database
CREATE DATABASE IF NOT EXISTS unisync;
USE unisync;

-- ============================================
-- USER TABLES
-- ============================================

-- Student Table
CREATE TABLE IF NOT EXISTS Student (
    SRN VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Dept VARCHAR(50) NOT NULL,
    Suspended BOOLEAN DEFAULT FALSE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (Email),
    INDEX idx_suspended (Suspended)
);

-- Admin Table
CREATE TABLE IF NOT EXISTS Admin (
    AdminId VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (Email)
);

-- ============================================
-- RESOURCE TABLES
-- ============================================

-- Category Table
CREATE TABLE IF NOT EXISTS Category (
    CategoryId INT PRIMARY KEY AUTO_INCREMENT,
    MainType VARCHAR(100) NOT NULL,
    SubType VARCHAR(100) NOT NULL,
    Description TEXT,
    INDEX idx_maintype (MainType)
);

-- Resource Table
CREATE TABLE IF NOT EXISTS Resource (
    ResourceId INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    ItemCondition VARCHAR(50) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    ListingType VARCHAR(50) NOT NULL,
    OwnerId VARCHAR(20) NOT NULL,
    CategoryId INT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (OwnerId) REFERENCES Student(SRN) ON DELETE CASCADE,
    FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId),
    INDEX idx_owner (OwnerId),
    INDEX idx_status (Status),
    INDEX idx_listingtype (ListingType),
    INDEX idx_category (CategoryId)
);

-- ============================================
-- TRANSACTION TABLES
-- ============================================

-- Transaction Base Table
CREATE TABLE IF NOT EXISTS Transaction (
    TransactionId INT PRIMARY KEY AUTO_INCREMENT,
    TransactionType VARCHAR(50) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_type (TransactionType),
    INDEX idx_status (Status)
);

-- BuySell Transaction Details
CREATE TABLE IF NOT EXISTS BuySellTransaction (
    TransactionId INT PRIMARY KEY,
    ResourceId INT NOT NULL,
    SellerId VARCHAR(20) NOT NULL,
    BuyerId VARCHAR(20) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (TransactionId) REFERENCES Transaction(TransactionId) ON DELETE CASCADE,
    FOREIGN KEY (ResourceId) REFERENCES Resource(ResourceId),
    FOREIGN KEY (SellerId) REFERENCES Student(SRN),
    FOREIGN KEY (BuyerId) REFERENCES Student(SRN),
    INDEX idx_seller (SellerId),
    INDEX idx_buyer (BuyerId),
    INDEX idx_resource (ResourceId)
);

-- LendBorrow Transaction Details
CREATE TABLE IF NOT EXISTS LendBorrowTransaction (
    TransactionId INT PRIMARY KEY,
    ResourceId INT NOT NULL,
    LenderId VARCHAR(20) NOT NULL,
    BorrowerId VARCHAR(20) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Penalty DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (TransactionId) REFERENCES Transaction(TransactionId) ON DELETE CASCADE,
    FOREIGN KEY (ResourceId) REFERENCES Resource(ResourceId),
    FOREIGN KEY (LenderId) REFERENCES Student(SRN),
    FOREIGN KEY (BorrowerId) REFERENCES Student(SRN),
    INDEX idx_lender (LenderId),
    INDEX idx_borrower (BorrowerId),
    INDEX idx_enddate (EndDate)
);

-- Barter Transaction Details
CREATE TABLE IF NOT EXISTS BarterTransaction (
    TransactionId INT PRIMARY KEY,
    OfferedResourceId INT NOT NULL,
    RequestedResourceId INT NOT NULL,
    ProposerId VARCHAR(20) NOT NULL,
    AccepterId VARCHAR(20) NOT NULL,
    FOREIGN KEY (TransactionId) REFERENCES Transaction(TransactionId) ON DELETE CASCADE,
    FOREIGN KEY (OfferedResourceId) REFERENCES Resource(ResourceId),
    FOREIGN KEY (RequestedResourceId) REFERENCES Resource(ResourceId),
    FOREIGN KEY (ProposerId) REFERENCES Student(SRN),
    FOREIGN KEY (AccepterId) REFERENCES Student(SRN),
    INDEX idx_proposer (ProposerId),
    INDEX idx_accepter (AccepterId)
);

-- ============================================
-- REVIEW TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS Review (
    ReviewId INT PRIMARY KEY AUTO_INCREMENT,
    Rating INT NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
    Comment TEXT,
    ReviewerId VARCHAR(20) NOT NULL,
    ResourceId INT NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ReviewerId) REFERENCES Student(SRN) ON DELETE CASCADE,
    FOREIGN KEY (ResourceId) REFERENCES Resource(ResourceId) ON DELETE CASCADE,
    INDEX idx_reviewer (ReviewerId),
    INDEX idx_resource (ResourceId),
    UNIQUE KEY unique_review (ReviewerId, ResourceId)
);

-- ============================================
-- REMINDER TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS Reminder (
    ReminderId INT PRIMARY KEY AUTO_INCREMENT,
    Message TEXT NOT NULL,
    Status VARCHAR(50) DEFAULT 'UNREAD',
    ReminderDate DATE NOT NULL,
    StudentId VARCHAR(20),
    TransactionId INT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StudentId) REFERENCES Student(SRN) ON DELETE CASCADE,
    FOREIGN KEY (TransactionId) REFERENCES Transaction(TransactionId) ON DELETE CASCADE,
    INDEX idx_student (StudentId),
    INDEX idx_status (Status),
    INDEX idx_date (ReminderDate)
);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Insert Sample Categories
INSERT INTO Category (MainType, SubType, Description) VALUES
('Textbooks', 'Engineering', 'Engineering textbooks and study materials'),
('Textbooks', 'Science', 'Science textbooks'),
('Textbooks', 'Arts', 'Arts and humanities books'),
('Electronics', 'Calculators', 'Scientific and graphing calculators'),
('Electronics', 'Laptops', 'Laptop computers'),
('Furniture', 'Study Desk', 'Study tables and desks'),
('Furniture', 'Chair', 'Study chairs'),
('Lab Equipment', 'Microscope', 'Laboratory microscopes'),
('Notes', 'Handwritten', 'Student handwritten notes'),
('Others', 'Miscellaneous', 'Other resources');

-- Insert Sample Students
INSERT INTO Student (SRN, Name, Email, Phone, Password, Dept) VALUES
('STU001', 'Rajesh Kumar', 'rajesh@student.edu', '9876543210', 'pass123', 'CSE'),
('STU002', 'Priya Sharma', 'priya@student.edu', '9876543211', 'pass123', 'ECE'),
('STU003', 'Amit Patel', 'amit@student.edu', '9876543212', 'pass123', 'ME'),
('STU004', 'Neha Gupta', 'neha@student.edu', '9876543213', 'pass123', 'CSE'),
('STU005', 'Vikram Singh', 'vikram@student.edu', '9876543214', 'pass123', 'Civil');

-- Insert Sample Admin
INSERT INTO Admin (AdminId, Name, Email, Phone, Password) VALUES
('ADMIN001', 'Administrator', 'admin@unisync.edu', '9999999999', 'admin123');

-- Insert Sample Resources
INSERT INTO Resource (Title, Description, ItemCondition, Status, ListingType, OwnerId, CategoryId) VALUES
('Data Structures & Algorithms', 'CLRS - Near mint condition', 'Good', 'AVAILABLE', 'SELL', 'STU001', 1),
('Signals and Systems', 'Simon Haykin - Slightly used', 'Good', 'AVAILABLE', 'LEND', 'STU002', 2),
('Scientific Calculator', 'Casio FX-991EX', 'Good', 'AVAILABLE', 'LEND', 'STU001', 4),
('Physics Notes - Mechanics', 'Comprehensive handwritten notes', 'Good', 'AVAILABLE', 'SELL', 'STU003', 9),
('Study Chair', 'Ergonomic study chair', 'Excellent', 'AVAILABLE', 'BARTER', 'STU004', 7);

-- ============================================
-- VIEWS (Optional - for reporting)
-- ============================================

-- View for All Transactions with Details
CREATE OR REPLACE VIEW TransactionSummary AS
SELECT 
    t.TransactionId,
    t.TransactionType,
    t.Status,
    t.CreatedAt,
    CASE 
        WHEN t.TransactionType = 'BUYSELL' THEN 
            (SELECT CONCAT(s1.Name, ' -> ', s2.Name) 
             FROM BuySellTransaction bst 
             JOIN Student s1 ON bst.SellerId = s1.SRN 
             JOIN Student s2 ON bst.BuyerId = s2.SRN 
             WHERE bst.TransactionId = t.TransactionId)
        WHEN t.TransactionType = 'LENDBORROW' THEN 
            (SELECT CONCAT(s1.Name, ' <- ', s2.Name) 
             FROM LendBorrowTransaction lbt 
             JOIN Student s1 ON lbt.LenderId = s1.SRN 
             JOIN Student s2 ON lbt.BorrowerId = s2.SRN 
             WHERE lbt.TransactionId = t.TransactionId)
    END AS Parties
FROM Transaction t;

-- View for Resource Availability Summary
CREATE OR REPLACE VIEW ResourceAvailability AS
SELECT 
    Status,
    COUNT(*) as Count,
    AVG(RATING_COUNT) as AvgRating
FROM Resource r
LEFT JOIN (
    SELECT ResourceId, COUNT(*) as RATING_COUNT
    FROM Review
    GROUP BY ResourceId
) rv ON r.ResourceId = rv.ResourceId
GROUP BY Status;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Create additional indexes for common queries
CREATE INDEX idx_transaction_date ON Transaction(CreatedAt);
CREATE INDEX idx_reminder_date ON Reminder(ReminderDate);
CREATE INDEX idx_buysell_price ON BuySellTransaction(Price);
CREATE INDEX idx_lendborrow_dates ON LendBorrowTransaction(StartDate, EndDate);

-- ============================================
-- TRIGGERS (Optional - for data integrity)
-- ============================================

-- Trigger to update resource status when BuySell transaction completes
DELIMITER $$
CREATE TRIGGER update_resource_on_buysell_complete
AFTER UPDATE ON BuySellTransaction
FOR EACH ROW
BEGIN
    IF (SELECT Status FROM Transaction WHERE TransactionId = NEW.TransactionId) = 'COMPLETED' THEN
        UPDATE Resource SET Status = 'SOLD' WHERE ResourceId = NEW.ResourceId;
    END IF;
END$$
DELIMITER ;

-- Trigger to update resource status when LendBorrow transaction initiates
DELIMITER $$
CREATE TRIGGER update_resource_on_lendborrow_initiate
AFTER INSERT ON LendBorrowTransaction
FOR EACH ROW
BEGIN
    UPDATE Resource SET Status = 'BORROWED' WHERE ResourceId = NEW.ResourceId;
END$$
DELIMITER ;

-- ============================================
-- SAMPLE QUERIES FOR TESTING
-- ============================================

/*
-- Get all available resources
SELECT * FROM Resource WHERE Status = 'AVAILABLE';

-- Get resources by category
SELECT r.* FROM Resource r 
JOIN Category c ON r.CategoryId = c.CategoryId 
WHERE c.MainType = 'Textbooks';

-- Get student's listed resources
SELECT * FROM Resource WHERE OwnerId = 'STU001';

-- Get reviews for a resource
SELECT r.ReviewId, r.Rating, r.Comment, s.Name as Reviewer
FROM Review r
JOIN Student s ON r.ReviewerId = s.SRN
WHERE r.ResourceId = 1;

-- Get pending transactions
SELECT * FROM Transaction WHERE Status = 'PENDING';

-- Get late borrow returns
SELECT lbt.*, datediff(curdate(), lbt.EndDate) as DaysLate
FROM LendBorrowTransaction lbt
JOIN Transaction t ON lbt.TransactionId = t.TransactionId
WHERE t.Status != 'COMPLETED' AND lbt.EndDate < curdate();

-- Get transaction statistics by student
SELECT 
    SellerId as StudentId,
    COUNT(*) as Total,
    SUM(CASE WHEN Status = 'COMPLETED' THEN 1 ELSE 0 END) as Completed
FROM BuySellTransaction bst
JOIN Transaction t ON bst.TransactionId = t.TransactionId
GROUP BY SellerId;
*/

-- End of UniSync Database Schema
