
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import numpy as np
from flask import Flask, request, jsonify
import csv
import io


app = Flask(__name__)

# Завантаження натренованої моделі
model = joblib.load('logistic_regression_model.pkl')

# Функція для обробки даних і прогнозування
def process_data():
    # Завантаження нових даних
    data = pd.read_csv('data.csv')

    # Кодування категоріальних даних (transaction_category)
    label_encoder = LabelEncoder()
    data['transaction_category_encoded'] = label_encoder.fit_transform(data['transaction_category'])

    # Конвертація дати в числовий формат (кількість секунд від Unix Epoch)
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])
    data['transaction_date_encoded'] = data['transaction_date'].astype('int64') / 10**9  # Конвертація у секунди

    # Вибір колонок для масштабування
    columns_to_scale = ['id', 'sender_id', 'receiver_id', 'transaction_date_encoded', 'transaction_amount', 'transaction_category_encoded']

    # Масштабування даних у діапазон (-120, 120)
    scaler = MinMaxScaler(feature_range=(-120, 120))
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

    # Додавання відсутніх ознак з випадковими значеннями
    missing_features = 30 - len(columns_to_scale)
    for i in range(missing_features):
        data[f'missing_feature_{i}'] = np.random.uniform(-120, 120, size=len(data))

    # Кодування всіх унікальних категорій (стрінгових значень) в унікальні числа в заданому діапазоні (-120, 120)
    unique_categories = data['transaction_category'].unique()
    category_mapping = {category: np.random.uniform(-120, 120) for category in unique_categories}
    data['transaction_category_mapped'] = data['transaction_category'].map(category_mapping)

    # Прогнозування класу (шахрайство або ні)
    X_new = data[columns_to_scale + [f'missing_feature_{i}' for i in range(missing_features)]].values
    predictions = model.predict(X_new)

    # Додавання результатів до датасету
    data['Class'] = predictions

    # Збереження результатів у новий CSV файл
    data.to_csv('transactions_with_predictions.csv', index=False)

    # Перевірка результату
    print("\nData with Predictions:")
    print(data.head())

@app.route('/data', methods=['POST'])
def receive_data():
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'text/csv':
        return jsonify({'message': 'Unsupported Media Type'}), 415
    
    # Отримати дані з запиту
    data = request.data.decode('utf-8')
    
    # Зберегти дані у файл CSV
    file_path = 'data.csv'
    
    # Список для зберігання рядків
    csv_lines = []
    
    # Читання даних з CSV
    input_stream = io.StringIO(data)
    csv_reader = csv.DictReader(input_stream)
    
    for row in csv_reader:
        csv_lines.append(row)
    
    # Записування у файл
    with open(file_path, 'a', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=csv_lines[0].keys())
        # Записуємо заголовки, якщо файл порожній
        if file.tell() == 0:
            csv_writer.writeheader()
        csv_writer.writerows(csv_lines)

    # Запуск обробки даних і прогнозування
    process_data()

    # Приклад відповіді
    return jsonify({'message': 'Data received, saved, and processed successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

