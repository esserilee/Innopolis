#!/bin/bash

# Пути к проектам
WEB_DIR=/Users/ekaterinalebedeva/Desktop/hh_app
BOT_DIR=/Users/ekaterinalebedeva/Desktop/telegram_bot
PYTHON3=/usr/bin/python3
STREAMLIT=/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit

#установка зависимостей для веб-приложения
echo "Установка зависимостей для веб-приложения"
cd $WEB_DIR
$PYTHON3 -m pip install --user -r requirements.txt

# Запуск Streamlit веб-приложения 
echo "=== Запуск Streamlit ==="
/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
STREAMLIT_PID=$!


echo "Ждем запуска Streamlit..."
while ! grep -q -E "Network URL|Local URL" streamlit.log; do
    sleep 1
done

# Получаем URL и открываем браузер
URL=$(grep -E "Network URL|Local URL" streamlit.log | tail -1 | awk '{print $3}')
echo "Веб-приложение готово: $URL"
open $URL

# Установка зависимостей для Telegram-бота 
echo " Установка зависимостей для Telegram-бота "
cd $BOT_DIR
$PYTHON3 -m pip install --user -r requirements.txt

# Запуск Telegram-бота 
echo "=== Запуск Telegram-бота ==="
$PYTHON3 bot.py

# Streamlit продолжает работать после завершения бота
echo "Бот завершился. Streamlit продолжает работу."
echo "Для остановки Streamlit используй: kill $STREAMLIT_PID"#!/bin/bash

# Пути к проектам
WEB_DIR=/Users/ekaterinalebedeva/Desktop/hh_app
BOT_DIR=/Users/ekaterinalebedeva/Desktop/telegram_bot
PYTHON3=/usr/bin/python3
STREAMLIT=/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit

# Установка зависимостей для веб-приложения 
echo "Установка зависимостей для веб-приложения "
cd $WEB_DIR
$PYTHON3 -m pip install --user -r requirements.txt

# Запуск Streamlit веб-приложения 
echo "Запуск Streamlit"
/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Ждем, пока Streamlit стартует
echo "Ждем запуска Streamlit..."
while ! grep -q -E "Network URL|Local URL" streamlit.log; do
    sleep 1
done

# Получаем URL и открываем браузер
URL=$(grep -E "Network URL|Local URL" streamlit.log | tail -1 | awk '{print $3}')
echo "Веб-приложение готово: $URL"
open $URL

# Установка зависимостей для Telegram-бота 
echo "=== Установка зависимостей для Telegram-бота ==="
cd $BOT_DIR
$PYTHON3 -m pip install --user -r requirements.txt

# Запуск Telegram-бота 
echo "Запуск Telegram-бота"
$PYTHON3 bot.py

# Streamlit продолжает работать после завершения бота
echo "Бот завершился. Streamlit продолжает работу."
echo "Для остановки Streamlit используй: kill $STREAMLIT_PID"#!/bin/bash

# Пути к проектам
WEB_DIR=/Users/ekaterinalebedeva/Desktop/hh_app
BOT_DIR=/Users/ekaterinalebedeva/Desktop/telegram_bot
PYTHON3=/usr/bin/python3
STREAMLIT=/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit

# Установка зависимостей для веб-приложения 
echo "Установка зависимостей для веб-приложения "
cd $WEB_DIR
$PYTHON3 -m pip install --user -r requirements.txt

#  Запуск Streamlit веб-приложения 
echo "Запуск Streamlit "
/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Ждем, пока Streamlit стартует
echo "Ждем запуска Streamlit..."
while ! grep -q -E "Network URL|Local URL" streamlit.log; do
    sleep 1
done

# Получаем URL и открываем браузер
URL=$(grep -E "Network URL|Local URL" streamlit.log | tail -1 | awk '{print $3}')
echo "Веб-приложение готово: $URL"
open $URL

#  Установка зависимостей для Telegram-бота 
echo "Установка зависимостей для Telegram-бота"
cd $BOT_DIR
$PYTHON3 -m pip install --user -r requirements.txt

#Запуск Telegram-бота 
echo "Запуск Telegram-бота"
$PYTHON3 bot.py

# Streamlit продолжает работать после завершения бота
echo "Бот завершился. Streamlit продолжает работу."
echo "Для остановки Streamlit используй: kill $STREAMLIT_PID"
#!/bin/bash

# Пути к проектам
WEB_DIR=/Users/ekaterinalebedeva/Desktop/hh_app
BOT_DIR=/Users/ekaterinalebedeva/Desktop/telegram_bot
PYTHON3=/usr/bin/python3
STREAMLIT=/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit

# Установка зависимостей для веб-приложения
echo "Установка зависимостей для веб-приложения"
cd $WEB_DIR
$PYTHON3 -m pip install --user -r requirements.txt

# Запуск Streamlit веб-приложения 
echo "Запуск Streamlit"
/Users/ekaterinalebedeva/Library/Python/3.9/bin/streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Ждем, пока Streamlit стартует
echo "Ждем запуска Streamlit..."
while ! grep -q -E "Network URL|Local URL" streamlit.log; do
    sleep 1
done

# Получаем URL и открываем браузер
URL=$(grep -E "Network URL|Local URL" streamlit.log | tail -1 | awk '{print $3}')
echo "Веб-приложение готово: $URL"
open $URL

#Установка зависимостей для Telegram-бота 
echo "Установка зависимостей для Telegram-бота"
cd $BOT_DIR
$PYTHON3 -m pip install --user -r requirements.txt

#Запуск Telegram-бота 
echo " Запуск Telegram-бота"
$PYTHON3 bot.py

# Streamlit продолжает работать после завершения бота
echo "Бот завершился. Streamlit продолжает работу."
echo "Для остановки Streamlit используй: kill $STREAMLIT_PID"
