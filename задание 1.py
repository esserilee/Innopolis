import pandas as pd
link = "https://raw.githubusercontent.com/YBI-Foundation/Dataset/main/Attention.csv"
DataFrame = pd.read_csv(link)

print("Количество столбцов:", len(DataFrame.columns))
print("Количество строк:", len(DataFrame))

print("\nТипы данных в столбцах:\n", DataFrame.dtypes)

print("\nУникальные элементы в каждом столбце:", DataFrame.nunique())

a = DataFrame.select_dtypes(include=['object']).columns
print("\nЧастота встречающихся элементов:")
for col in a:
    print(f"\nСтолбец '{col}':")
    print(DataFrame[col].value_counts())

b = DataFrame.select_dtypes(include=['int64', 'float64']).columns
for col in b:
    print(f"\nСтолбец '{col}':")
    print(f"Минимум: {DataFrame[col].min()}")
    print(f"Среднее: {DataFrame[col].mean():.2f}")
    print(f"Медиана: {DataFrame[col].median()}")
    print(f"Максимум: {DataFrame[col].max()}")