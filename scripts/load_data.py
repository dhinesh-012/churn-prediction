# scripts/load_data.py
import argparse
import psycopg2
import os

def run(create_sql_path, csv_path, db_conn_str):
    # connect
    conn = psycopg2.connect(db_conn_str)
    cur = conn.cursor()

    # run create table SQL
    with open(create_sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()

    # empty table (safety)
    cur.execute("TRUNCATE TABLE customers;")
    conn.commit()

    # COPY CSV into table (explicit column order)
    copy_sql = """
    COPY customers(
        customerid, gender, seniorcitizen, partner, dependents, tenure,
        phoneservice, multiplelines, internetservice, onlinesecurity,
        onlinebackup, deviceprotection, techsupport, streamingtv,
        streamingmovies, contract, paperlessbilling, paymentmethod,
        monthlycharges, totalcharges, churn
    )
    FROM STDIN WITH CSV HEADER DELIMITER ',' NULL '';
    """

    with open(csv_path, 'r', encoding='utf-8') as f:
        cur.copy_expert(copy_sql, f)
    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to cleaned CSV (data/Telco-Customer-Churn-Cleaned.csv)")
    parser.add_argument("--create-sql", default="sql/create_tables.sql", help="Path to create_tables.sql")
    parser.add_argument("--db", required=True, help="psycopg2 connection string e.g. \"dbname=churn_db user=churn_user password=pass host=localhost port=5432\"")
    args = parser.parse_args()
    run(args.create_sql, args.csv, args.db)
