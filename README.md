# UniSync — Student Resource Exchange Platform

> A full-stack student marketplace for buying, selling, lending, borrowing, and bartering academic resources. Built with Java (OOAD patterns) + Streamlit (Python UI) + MySQL.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Team & Responsibilities](#team--responsibilities)
- [Architecture](#architecture)
- [OOAD Design Patterns](#ooad-design-patterns)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup & Running](#setup--running)
- [API Endpoints](#api-endpoints)
- [Deliverables](#deliverables)

---

## Project Overview

UniSync is a campus-level peer-to-peer resource sharing platform. Students can:

- **Sell / Buy** textbooks, electronics, and equipment
- **Lend / Borrow** items with due-date tracking and late penalties
- **Barter** items directly with other students
- **Review** resources they have transacted with
- **Receive reminders** for upcoming return deadlines

Administrators can manage students (suspend/activate/delete), remove inappropriate listings, and view platform-wide transaction statistics.

---

## Team & Responsibilities

| Member | Modules | Classes |
|--------|---------|---------|
| **Meenakshi** | Review, Student, Resource | `Review`, `Student`, `User`, `Resource`, `ResourceStatus`, `ListingType`, `ReviewDAO`, `StudentDAO`, `ResourceDAO` + impls, `ReviewService`, `StudentService`, `ResourceService`, `ReviewMenu`, `StudentMenu`, `ResourceMenu` |
| **Nam** | Category, Transaction, Reminder + UI | `Category`, `Transaction`, `TransactionStatus`, `BarterTransaction`, `Reminder`, `TransactionFactory`, `TransactionDAO` + impl, `TransactionService`, `ReminderService`, `ReminderObserver`, `ReminderSubject`, `StudentNotification`, `SessionManager`|
| **Neema** | BuySell, LendBorrow, Strategy, Admin | `BuySellTransaction`, `LendBorrowTransaction`, `PenaltyStrategy`, `StandardPenalty`, `PremiumPenalty`, `Admin`, `AdminService`, `AdminController`, `TransactionController`, `AdminMenu`, `TransactionMenu`, `MainMenu` |


## Database Schema

Key tables and relationships:

| Table | Description |
|-------|-------------|
| `Student` | Registered students (SRN, Name, Email, Dept, Suspended) |
| `Admin` | Admin accounts |
| `Category` | Resource categories (MainType / SubType) |
| `Resource` | Listed items with Status and ListingType (SELL/LEND/BARTER) |
| `Transaction` | Base transaction record (type + status) |
| `BuySellTransaction` | Extends Transaction — Price, Seller, Buyer |
| `LendBorrowTransaction` | Extends Transaction — Dates, Penalty |
| `BarterTransaction` | Extends Transaction — OfferedResource, RequestedResource |
| `Review` | 1–5 star ratings on completed transactions |
| `Reminder` | Due-date notifications linked to students + transactions |

