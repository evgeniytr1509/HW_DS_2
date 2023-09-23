import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np  # Для использования значения NaN

# URL-адрес веб-страницы с таблицей данных
url = "https://uk.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B8"

# Отправка GET-запроса и получение содержимого страницы
response = requests.get(url)

# Парсинг HTML-кода страницы с помощью BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Нахождение и чтение таблицы(-ц) с помощью Pandas
tables = pd.read_html(str(soup))


selected_table = tables[12]  #  выбор  таблицы 
print(selected_table)


print ("**************")
#  1 первые 5 строк таблицы
first_5_rows = selected_table.head(5)
print(first_5_rows)


# 2 Определение количества строк и столбцов в DataFrame
rows, columns = selected_table.shape
print(f"Количество строк: {rows}")
print(f"Количество столбцов: {columns}")


# 3 Замена значений "—" на NaN
selected_table = selected_table.replace("—", np.nan)
print (selected_table)

# 4 Определение типов данных столбцов
column_types = selected_table.dtypes
print(column_types)


# 5 Замена значений "—" на NaN
selected_table = selected_table.replace("—", np.nan)
# Преобразование нечисловых колонок в числовые (тип float), пропуская строки заголовка
non_numeric_columns = selected_table.columns[selected_table.dtypes == 'object']  # Выбор нечисловых колонок
selected_table[non_numeric_columns] = selected_table[non_numeric_columns].apply(pd.to_numeric, errors='coerce', axis=0)


# 6 Подсчет количества пропусков в каждой колонке
missing_values = selected_table.isnull().sum()

# Подсчет доли пропусков в каждой колонке
total_rows = len(selected_table)
missing_percent = (missing_values / total_rows) * 100

# Вывод доли пропусков в каждой колонке
print("Доля пропусков в каждой колонке:")
print(missing_percent)


# 7 Удаление последней строки (данных по всей стране)
selected_table = selected_table.drop(selected_table.index[-1])

# 8 Замена NaN средними значениями столбцов
selected_table = selected_table.fillna(selected_table.mean())


# 9 Отримайте список регіонів, де рівень народжуваності у 2019 році був вищим за середній по Україні
# Вычисление среднего уровня рождаемости в 2019 году по Украине
average_birth_rate_ukraine_2019 = selected_table['2019'].mean()

# Выбор регионов, где уровень рождаемости в 2019 году был выше среднего по Украине
regions_above_average = selected_table[selected_table['2019'] > average_birth_rate_ukraine_2019]

# Получение списка регионов (2019 год)
regions_list = regions_above_average.iloc[:, 8].tolist()

# Вывод списка регионов
print("Регіони з вищим рівнем народжуваності в 2019 році за середнім по Україні:")
print (average_birth_rate_ukraine_2019)
print(regions_list)



# Нахождение региона с наивысшей рождаемостью в 2014 году
region_with_highest_birth_rate_2014 = selected_table[selected_table['2014'] == selected_table['2014'].max()]
highest_birth_rate_region_2014 = region_with_highest_birth_rate_2014.iloc[0]['Регіон']

print("Регіон з найвищою народжуваністю в 2014 році:")
print(highest_birth_rate_region_2014)
print(region_with_highest_birth_rate_2014)





