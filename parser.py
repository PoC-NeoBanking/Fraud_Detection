import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
# Load environment variables (assuming .env file exists)
load_dotenv()

# Database connection details
password = os.environ["PASSWORD"]
dbname = "Neobanking_BD"
user = "postgres"

try:
    connect = psycopg2.connect(dbname=dbname, user=user, password=password)
    print("Connected to PostgreSQL database successfully!")

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL database: {e}")
    exit()

with connect.cursor() as cursor:

    # Define export directory (adjust as needed)
    export_dir = os.path.join('src')
    os.makedirs(export_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Export data from "users" table
    table_name = "users"
    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[col.name for col in cursor.description])
    df.to_csv(os.path.join(export_dir, f"{table_name}.csv"), index=False)
    print(f"Data from '{table_name}' table exported to CSV file.")

    # Export data from "transactions" table
    table_name = "transactions"
    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[col.name for col in cursor.description])
    df.to_csv(os.path.join(export_dir, f"{table_name}.csv"), index=False)
    print(f"Data from '{table_name}' table exported to CSV file.")

if connect:
    connect.commit()
    connect.close()

print("Database operations completed.")
 # type: ignore

