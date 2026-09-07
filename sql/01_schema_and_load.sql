-- ============================================================
-- E-Commerce Business Analytics - MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

CREATE TABLE IF NOT EXISTS customers (
    CustomerID      VARCHAR(20) PRIMARY KEY,
    CustomerName    VARCHAR(100),
    Segment         VARCHAR(30),
    Region          VARCHAR(20),
    City            VARCHAR(50),
    JoinDate        DATE
);

CREATE TABLE IF NOT EXISTS products (
    ProductID       VARCHAR(20) PRIMARY KEY,
    ProductName     VARCHAR(100),
    Category        VARCHAR(50),
    UnitCost        DECIMAL(10,2),
    UnitPrice       DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS orders (
    OrderID         VARCHAR(20),
    OrderDate       DATE,
    CustomerID      VARCHAR(20),
    ProductID       VARCHAR(20),
    ProductName     VARCHAR(100),
    Category        VARCHAR(50),
    Quantity        INT,
    UnitPrice       DECIMAL(10,2),
    Discount        DECIMAL(5,2),
    Sales           DECIMAL(12,2),
    Profit          DECIMAL(12,2),
    ShipMode        VARCHAR(20),
    DeliveryDays    INT,
    DeliveryDate    DATE,
    Returned        VARCHAR(5),
    CustomerRating  INT
);

-- ============================================================
-- Import order (MySQL Workbench Table Data Import Wizard):
-- 1. customers.csv  → customers
-- 2. products.csv   → products
-- 3. orders.csv     → orders
-- ============================================================
