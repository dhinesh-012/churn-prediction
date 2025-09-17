# Customer Churn Prediction (Postgres + ML)

## Quick start

1. Put cleaned CSV in `data/Telco-Customer-Churn-Cleaned.csv`.
2. Create DB & user in PostgreSQL:
   ```sql
   CREATE USER churn_user WITH PASSWORD 'yourpassword';
   CREATE DATABASE churn_db;
   GRANT ALL PRIVILEGES ON DATABASE churn_db TO churn_user;

   
   
<img width="544" height="434" alt="Screenshot 2025-09-17 200638" src="https://github.com/user-attachments/assets/79bb228a-9ade-4d75-b695-356ed1f8a1d4" />
<img width="425" height="91" alt="Screenshot 2025-09-17 203554" src="https://github.com/user-attachments/assets/e8544caf-de6d-4e38-96b3-37ae915b6803" />
