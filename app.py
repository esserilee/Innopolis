import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

from urllib.parse import quote_plus


st.set_page_config(page_title="Подбор вакансий", layout="centered")


@st.cache_data
def load_data():
    import itertools

    encodings = ["utf-8", "cp1251", "latin1"]
    seps = [",", ";", "\t"]

    last_error = None

    for enc, sep in itertools.product(encodings, seps):
        try:
            df = pd.read_csv(
                "vacancies_hh.csv",
                encoding=enc,
                sep=sep,
                engine="python",
                on_bad_lines="skip"
            )

            # чистим названия колонок
            df.columns = [
                col.strip().lower().replace("\ufeff", "")
                for col in df.columns
            ]

            # если нашли нужный столбец – используем этот вариант
            if "title" in df.columns:
                df["title"] = df["title"].astype(str).str.lower().str.strip()
                st.info(f"Файл загружен (encoding={enc}, sep='{sep}')")
                return df

        except Exception as e:
            last_error = e
            continue

    # если сюда дошли – ни один вариант не подошёл
    st.error(
        "Не удалось автоматически распознать структуру файла vacancies_hh.csv.\n"
        "Проверьте, что в первой строке есть заголовки колонок и среди них есть колонка "
        "'title' (название вакансии). "
        f"Последняя ошибка чтения: {last_error}"
    )
    st.stop()


df = load_data()


# предобработка

def unify_salary(row):
    s_from = row.get("salary_from")
    s_to = row.get("salary_to")

    if pd.isna(s_from) and pd.isna(s_to):
        return None
    if pd.isna(s_to):
        return s_from
    if pd.isna(s_from):
        return s_to
    return (s_from + s_to) / 2


df["salary_mid"] = df.apply(unify_salary, axis=1)


# TF-IDF

vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
tfidf_matrix = vectorizer.fit_transform(df["title"])


# модель

mask = df["salary_mid"].notna()
X = tfidf_matrix[mask.values]
y = df.loc[mask, "salary_mid"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)




def experience_code(exp_years):
    if exp_years is None:
        return None
    if exp_years < 1:
        return "noExperience"
    if exp_years < 3:
        return "between1And3"
    if exp_years < 6:
        return "between3And6"
    return "moreThan6"


def generate_hh_link(role, salary=None, exp_years=None):
    base = "https://hh.ru/search/vacancy?"
    params = []

    if role:
        params.append(f"text={quote_plus(role)}")

    if salary is not None:
        try:
            salary = int(salary)
            params.append(f"salary={salary}")
        except:
            pass

    code = experience_code(exp_years)
    if code:
        params.append(f"experience={code}")

    return base + "&".join(params)


def get_vacancies(role_query, min_salary=None, min_exp=None, city=None, top_n=10):
    query_vec = vectorizer.transform([role_query.lower()])
    sim = cosine_similarity(query_vec, tfidf_matrix).flatten()

    df_local = df.copy()
    df_local["similarity"] = sim

    if min_salary:
        df_local = df_local[df_local["salary_mid"].fillna(0) >= min_salary]

    if min_exp:
        df_local = df_local[df_local["experience_years"].fillna(0) >= min_exp]

    if city:
        df_local = df_local[df_local["city"].str.lower() == city.lower()]

    df_local = df_local.sort_values(by=["similarity", "salary_mid"], ascending=False)

    result = df_local[[
        "title", "city", "salary_from", "salary_to",
        "salary_mid", "experience_years", "similarity"
    ]].head(top_n)

    link = generate_hh_link(role_query, min_salary, min_exp)
    return result, link


# интерфейс

st.title("🔎 Подбор вакансий")

st.markdown("### Введите параметры для поиска")

role = st.text_input("Должность (например: аналитик данных)")
salary = st.text_input("Минимальная зарплата, руб.")
exp = st.text_input("Минимальный опыт (в годах)")
city = st.text_input("Город (например: Москва)")

if st.button("Найти вакансии"):

    min_salary = int(salary) if salary.isdigit() else None
    min_exp = float(exp.replace(",", ".")) if exp else None
    city = city if city else None

    table, link = get_vacancies(role, min_salary, min_exp, city)

    st.subheader("🔗 Ссылка на hh.ru")
    st.write(link)

    st.subheader("📋 Подходящие вакансии")
    st.dataframe(table)

    st.subheader("📊 Качество ML-модели (предсказание зарплаты)")
    st.write(f"R² = {r2:.3f}")
    st.write(f"MAE = {int(mae)} руб.")


st.markdown("---")
st.caption("Прототип веб-приложения для подбора вакансий на основе анализа данных и ML")
df = load_data()

