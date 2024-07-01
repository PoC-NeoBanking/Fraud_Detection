import pandas as pd
from sklearn.model_selection import train_test_split

# Завантажуємо CSV файл
file_path = 'src/transactions.csv'
df = pd.read_csv(file_path)

# Розділяємо дані на тренувальний і тестувальний набори (наприклад, у співвідношенні 80/20)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Зберігаємо тренувальний і тестувальний набори у окремі CSV файли
train_df.to_csv('train_trans.csv', index=False)
test_df.to_csv('test_trans.csv', index=False)


# Завантаження CSV файлу
file_path = 'train_trans.csv'
df = pd.read_csv(file_path)

# Додавання нової колонки detected_fraud зі значеннями False
df['detected_fraud'] = False

# Зберігання оновленого DataFrame у CSV файлі
updated_file_path = 'train_trans.csv'
df.to_csv(updated_file_path, index=False)
