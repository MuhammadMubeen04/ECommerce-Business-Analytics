-- ============================================================
-- E-Commerce Business Analytics - Key SQL Queries (MySQL)
-- ============================================================

USE ecommerce_analytics;

-- 1. OVERALL KPIs
SELECT 
    COUNT(DISTINCT OrderID) AS total_orders,
    COUNT(DISTINCT CustomerID) AS total_customers,
    ROUND(SUM(Sales), 2) AS total_revenue,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(Sales), 2) AS avg_order_value,
    ROUND(SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_rate_pct,
    ROUND(AVG(CustomerRating), 2) AS avg_rating
FROM orders;


-- 2. MONTHLY TREND
SELECT 
    YEAR(OrderDate) AS year,
    MONTH(OrderDate) AS month,
    DATE_FORMAT(OrderDate, '%Y-%m') AS year_month,
    COUNT(DISTINCT OrderID) AS orders,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM orders
GROUP BY YEAR(OrderDate), MONTH(OrderDate), DATE_FORMAT(OrderDate, '%Y-%m')
ORDER BY year, month;


-- 3. CATEGORY PERFORMANCE
SELECT 
    Category,
    COUNT(DISTINCT OrderID) AS orders,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_rate_pct,
    ROUND(AVG(CustomerRating), 2) AS avg_rating
FROM orders
GROUP BY Category
ORDER BY revenue DESC;


-- 4. TOP PRODUCTS BY PROFIT
SELECT 
    ProductName,
    Category,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY ProductName, Category
ORDER BY profit DESC
LIMIT 15;


-- 5. DISCOUNT IMPACT ON PROFIT
SELECT 
    CASE 
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.10 THEN '1-10%'
        WHEN Discount <= 0.20 THEN '11-20%'
        ELSE '21%+'
    END AS discount_band,
    COUNT(*) AS order_lines,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(CustomerRating), 2) AS avg_rating
FROM orders
GROUP BY 
    CASE 
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.10 THEN '1-10%'
        WHEN Discount <= 0.20 THEN '11-20%'
        ELSE '21%+'
    END
ORDER BY MIN(Discount);


-- 6. RETURN RATE BY CATEGORY
SELECT 
    Category,
    COUNT(*) AS total_lines,
    SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END) AS returned_lines,
    ROUND(SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY Category
ORDER BY return_rate_pct DESC;


-- 7. TOP CUSTOMERS BY REVENUE
SELECT 
    o.CustomerID,
    c.CustomerName,
    c.Segment,
    c.Region,
    COUNT(DISTINCT o.OrderID) AS orders,
    ROUND(SUM(o.Sales), 2) AS total_revenue,
    ROUND(SUM(o.Profit), 2) AS total_profit
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
GROUP BY o.CustomerID, c.CustomerName, c.Segment, c.Region
ORDER BY total_revenue DESC
LIMIT 15;


-- 8. REGION PERFORMANCE
SELECT 
    c.Region,
    COUNT(DISTINCT o.OrderID) AS orders,
    COUNT(DISTINCT o.CustomerID) AS customers,
    ROUND(SUM(o.Sales), 2) AS revenue,
    ROUND(SUM(o.Profit), 2) AS profit,
    ROUND(SUM(o.Profit) / SUM(o.Sales) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY revenue DESC;


-- 9. SHIP MODE & DELIVERY
SELECT 
    ShipMode,
    COUNT(*) AS shipments,
    ROUND(AVG(DeliveryDays), 1) AS avg_delivery_days,
    ROUND(AVG(CustomerRating), 2) AS avg_rating,
    ROUND(SUM(CASE WHEN Returned = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM orders
GROUP BY ShipMode
ORDER BY shipments DESC;


-- 10. CUSTOMER RATING DISTRIBUTION
SELECT 
    CustomerRating,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) AS pct
FROM orders
GROUP BY CustomerRating
ORDER BY CustomerRating;
