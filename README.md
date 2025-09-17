# Customer Churn Prediction (Postgres + ML)

## Quick start

1. Put cleaned CSV in `data/Telco-Customer-Churn-Cleaned.csv`.
2. Create DB & user in PostgreSQL:
   ```sql
   CREATE USER churn_user WITH PASSWORD 'yourpassword';
   CREATE DATABASE churn_db;
   GRANT ALL PRIVILEGES ON DATABASE churn_db TO churn_user;
