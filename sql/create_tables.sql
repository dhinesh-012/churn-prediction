-- sql/create_tables.sql
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customerid VARCHAR PRIMARY KEY,
    gender VARCHAR,
    seniorcitizen INT,
    partner VARCHAR,
    dependents VARCHAR,
    tenure INT,
    phoneservice VARCHAR,
    multiplelines VARCHAR,
    internetservice VARCHAR,
    onlinesecurity VARCHAR,
    onlinebackup VARCHAR,
    deviceprotection VARCHAR,
    techsupport VARCHAR,
    streamingtv VARCHAR,
    streamingmovies VARCHAR,
    contract VARCHAR,
    paperlessbilling VARCHAR,
    paymentmethod VARCHAR,
    monthlycharges NUMERIC,
    totalcharges NUMERIC,
    churn VARCHAR
);
