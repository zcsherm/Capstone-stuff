-- Assignment 4

CREATE or REPLACE TABLE Customers (
  CustomerID int NOT NULL AUTO_INCREMENT,
  CustomerName varchar(50),
  AddressLine1 varchar(50),
  AddressLine2 varchar(50),
  City varchar(50),
  State varchar(50),
  PostalCode varchar(50),
  YTDPurchases decimal(19,2),
  PRIMARY KEY (CustomerID)
);

-- Display the Customers table and describe it
SHOW TABLES;
DESCRIBE Customers;

-- Populate Customers with basic info
INSERT INTO Customers ('CustomerName', 'AddressLine1', 'City', 'State', 'PostalCode')
VALUES ('Bike World', '60025 Bollinger Canyon Road', 'San Ramon', 'California', '94583'),
('Metro Sports', '482505 Warm Springs Blvd.', 'Fremont', 'California', '94536'),
('Johnny Sports', '1212 SE 93rd Ave.', 'Gladstone', 'Oregon', '97045');

-- Display all rows from  Customers
SELECT * FROM Customers;

-- Display ID and name for each person whose zip is 94536
SELECT CustomerID, CustomerName FROM Customers WHERE PostalCode = '94536';

-- Assignment 6

CREATE TABLE TermsCode (
  TermsCodeID varchar(50) NOT NULL,
  Description varchar(50),
  PRIMARY KEY (TermsCodeID)
);

-- Populate Terms Code categories
INSERT INTO TermsCode ('TermsCodeID', 'Description')
VALUES ('NET30', 'Payment due in 30 days.'),
('NET15', 'Payment due in 15 days.'),
('210NET30', '2% discount in 10 days Net 30');

-- Create a table for invoices
CREATE TABLE Invoices (
  InvoiceID int AUTO_INCREMENT,
  CustomerID int,
  InvoiceDate datetime,
  TermsCodeID varchar(50),
  TotalDue decimal(19,2),
  PRIMARY KEY (InvoiceID),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
  FOREIGN KEY (TermsCodeID) REFERENCES TermsCode(TermsCodeID)
);

-- Populate data for invoices
INSERT INTO Invoices ('CustomerID', 'InvoiceDate', 'TotalDue', 'TermsCodeID')
VALUES (2, '20140207', 2388.98, 'NET30'),
(1, '20140202', 2443.35, '210NET30'),
(1, '20140209', 8752.32, 'NET30');
