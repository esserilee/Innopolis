import logging
import pandas as pd

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote_plus



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)




df = pd.read_csv("vacancies_hh.csv", encoding="utf-8")
df["title"] = df["title"].astype(str).str.lower().str.strip()

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



vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2)
tfidf_matrix = vectorizer.fit_transform(df["title"])




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
            salary_int = int(salary)
            params.append(f"salary={salary_int}")
        except ValueError:
            pass

    code = experience_code(exp_years)
    if code:
        params.append(f"experience={code}")

    return base + "&".join(params)


def get_vacancies(role_query, min_salary=None, min_exp=None, city=None, top_n=5):
    q = role_query.lower().strip()
    query_vec = vectorizer.transform([q])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    df_local = df.copy()
    df_local["similarity"] = sim_scores

    if min_salary is not None:
        df_local = df_local[df_local["salary_mid"].fillna(0) >= min_salary]

    if min_exp is not None:
        df_local = df_local[df_local["experience_years"].fillna(0) >= min_exp]

    if city is not None:
        df_local = df_local[df_local["city"].str.lower() == city.lower()]

    df_local = df_local.sort_values(
        by=["similarity", "salary_mid"],
        ascending=False
    )

    result = df_local[[
        "title",
        "city",
        "salary_from",
        "salary_to",
        "salary_mid",
        "experience_years",
        "similarity",
    ]].head(top_n)

    hh_link = generate_hh_link(role_query, min_salary, min_exp)
    return result, hh_link




ROLE, SALARY, EXP, CITY = range(4)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для подбора вакансий.\n\n"
        "Давай начнем. Напиши, на какую должность ты хочешь искать вакансии:"
    )
    return ROLE


async def ask_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["role"] = update.message.text.strip()
    await update.message.reply_text(
        "Отлично! Теперь укажи минимальную зарплату (в рублях),\n"
        "или напиши '-' если не важно:"
    )
    return SALARY


async def ask_exp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    salary_text = update.message.text.strip()

    if salary_text == "-" or not salary_text:
        context.user_data["min_salary"] = None
    else:
        try:
            context.user_data["min_salary"] = int(salary_text)
        except ValueError:
            context.user_data["min_salary"] = None

    await update.message.reply_text(
        "Сколько лет опыта у тебя есть? (можно дробное число, например 1.5) "
        "или напиши '-' если не важно:"
    )
    return EXP


async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exp_text = update.message.text.strip()

    if exp_text == "-" or not exp_text:
        context.user_data["min_exp"] = None
    else:
        try:
            context.user_data["min_exp"] = float(exp_text.replace(",", "."))
        except ValueError:
            context.user_data["min_exp"] = None

    await update.message.reply_text(
        "В каком городе ищем вакансии? Напиши город или '-' если любой/удаленно:"
    )
    return CITY


async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city_text = update.message.text.strip()
    if city_text == "-" or not city_text:
        city = None
    else:
        city = city_text

    role = context.user_data.get("role")
    min_salary = context.user_data.get("min_salary")
    min_exp = context.user_data.get("min_exp")

    table, link = get_vacancies(
        role_query=role,
        min_salary=min_salary,
        min_exp=min_exp,
        city=city,
        top_n=5,
    )

    text_lines = []

    text_lines.append("Ссылка на поиск на hh.ru:\n" + link + "\n")
    text_lines.append("Подходящие вакансии:\n")

    if table.empty:
        text_lines.append("Ничего не найдено по заданным параметрам")
    else:
        for _, row in table.iterrows():
            sf = row["salary_from"]
            st = row["salary_to"]
            salary_str = ""
            if not pd.isna(sf) and not pd.isna(st):
                salary_str = f"{int(sf)}–{int(st)} руб."
            elif not pd.isna(sf):
                salary_str = f"от {int(sf)} руб."
            elif not pd.isna(st):
                salary_str = f"до {int(st)} руб."
            else:
                salary_str = "зарплата не указана"

            line = (
                f"• {row['title']} — {row['city']}\n"
                f"  Зарплата: {salary_str}\n"
                f"  Опыт: {row['experience_years']} лет\n"
            )
            text_lines.append(line)

    await update.message.reply_text("\n".join(text_lines))
    await update.message.reply_text("Чтобы начать новый поиск — напиши /start")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог завершён. Чтобы начать снова, напиши /start.")
    return ConversationHandler.END




def main():

    BOT_TOKEN = "8537294575:AAECVN1VmTcUZPyl5LeozVywS34_QZ-ebxA"

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_salary)],
            SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_exp)],
            EXP: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_results)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
