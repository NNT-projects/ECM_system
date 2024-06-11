import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Пример данных
data = [
    {"reportts": "2019-07-23 13:41:24", "acnum": "VQ-BDU", "pos": "2", "acct": "-20.0", "alt": "2330.0"},
    {"reportts": "2019-07-23 13:41:24", "acnum": "VQ-BDU", "pos": "1", "acct": "-20.0", "alt": "2330.0"},
    {"reportts": "2019-07-23 18:30:13", "acnum": "VQ-BDU", "pos": "1", "acct": "-20.0", "alt": "2365.0"},
    {"reportts": "2019-07-23 18:30:13", "acnum": "VQ-BDU", "pos": "2", "acct": "-20.0", "alt": "2365.0"},
    {"reportts": "2019-07-24 01:32:58", "acnum": "VQ-BDU", "pos": "1", "acct": "-20.0", "alt": "3710.0"},
    {"reportts": "2019-07-24 01:32:58", "acnum": "VQ-BDU", "pos": "2", "acct": "-20.0", "alt": "3710.0"},
    {"reportts": "2019-07-25 09:10:48", "acnum": "VQ-BDU", "pos": "2", "acct": "-20.0", "alt": "1663.0"}
]

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование столбцов в соответствующие типы данных
df['reportts'] = pd.to_datetime(df['reportts'])
df['alt'] = df['alt'].astype(float)

# Создание графика
plt.figure(figsize=(17, 6))
sns.lineplot(x='reportts', y='alt', hue='pos', data=df, marker='o')

# Настройка меток осей и заголовка
plt.xlabel('Time')
plt.ylabel('Altitude')
plt.title('Altitude Over Time for Different Positions')

# Добавление сетки
plt.grid(True)

# Отображение графика
plt.show()
