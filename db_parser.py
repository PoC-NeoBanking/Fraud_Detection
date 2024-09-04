import psycopg2
import requests
import csv
import io
import json
import os
from dotenv import load_dotenv

load_dotenv()

password = os.environ["PASSWORD"]
dbname = "Neobanking_BD"
user = "postgres"

def send_to_api(data):
    url = "http://127.0.0.1:5000/data"  # URL вашої Flask API
    headers = {'Content-Type': 'text/csv'}
    
    # Переконатися, що data є словником
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    # Конвертуємо словник у формат CSV
    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=data.keys())
    csv_writer.writeheader()
    csv_writer.writerow(data)
    
    csv_data = output.getvalue()
    output.close()
    
    response = requests.post(url, headers=headers, data=csv_data)
    print(f"Response: {response.status_code} - {response.text}")
    return response.status_code == 200  # Повертає True, якщо запит успішний

def process_queue():
    conn = psycopg2.connect(f"dbname={dbname} user={user} password={password}")
    cursor = conn.cursor()

    # Отримати всі записи з таблиці
    cursor.execute("SELECT * FROM api_queue")
    records = cursor.fetchall()

    if not records:
        print("Черга порожня.")
        return

    all_successful = True

    # Обробка кожного запису
    for record in records:
        id, sender_id, receiver_id, transaction_date, transaction_amount, transaction_category = record
        
        # Конвертуємо значення у рядки для CSV
        data = {
            "id": str(id),
            "sender_id": str(sender_id),
            "receiver_id": str(receiver_id),
            "transaction_date": transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            "transaction_amount": str(transaction_amount),
            "transaction_category": transaction_category
        }
        if not send_to_api(data):
            all_successful = False
            print(f"Помилка при обробці запису ID: {id}")
            break  # Зупиняємо процес, якщо хоча б один запит не був успішним

    # Якщо всі запити успішні, очищуємо чергу
    if all_successful:
        cursor.execute("TRUNCATE TABLE api_queue")
        conn.commit()
        print("Успішно оброблено всі записи. Чергу очищено.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    process_queue()
