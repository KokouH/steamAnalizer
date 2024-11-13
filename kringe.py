import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Генерация примера данных
np.random.seed(0)
data_length = 60
data = np.random.normal(loc=0, scale=1, size=data_length)
data[20] = 10  # Всплеск
data[50] = -10  # Всплеск

# Создание DataFrame
df = pd.DataFrame(data, columns=['Value'])

# Параметры для определения всплесков
window_size = 10
threshold_multiplier = 2.5  # Определяет чувствительность к всплескам

# Вычисление скользящего среднего и стандартного отклонения
df['Rolling_Mean'] = df['Value'].rolling(window=window_size).mean()
df['Rolling_Std'] = df['Value'].rolling(window=window_size).std()

# Определение всплесков

df['Spike'] = (df['Value'] > (df['Rolling_Mean'] + threshold_multiplier * df['Rolling_Std'])) | \
              (df['Value'] < (df['Rolling_Mean'] - threshold_multiplier * df['Rolling_Std']))

# Визуализация данных и всплесков
plt.figure(figsize=(12, 6))
plt.plot(df['Value'], label='Value', color='blue')
plt.plot(df['Rolling_Mean'], label='Rolling Mean', color='orange')
plt.fill_between(df.index, df['Rolling_Mean'] + threshold_multiplier * df['Rolling_Std'],
                 df['Rolling_Mean'] - threshold_multiplier * df['Rolling_Std'], color='gray', alpha=0.5)
plt.scatter(df.index[df['Spike']], df['Value'][df['Spike']], color='red', label='Spikes', zorder=5)
plt.title('Spike Detection in Time Series Data')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.show()


