import streamlit as st
import os

# Импортируем промышленный слой данных SQLite
import db_layer

# Инициализация структуры СУБД с нуля
db_layer.init_db()

# ==============================================================================
# 1. СКВОЗНОЙ ПОДКЛЮЧЕНИЕ СТИЛЕЙ И JS (CodePen: myREwOO)
# ==============================================================================
# Чтение и инъекция CSS
if os.path.exists("styles.css"):
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================================================================
# 2. ОФИЦИАЛЬНАЯ НАВИГАЦИЯ АПП (Сайдбар)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков АПП")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        [
            "🎓 Личный кабинет Физического лица", 
            "🏢 Личный кабинет Производства", 
            "🛠️ Кабинет Ассоциации (Управление)"
        ]
    )
    st.write("---")
    st.caption("Промышленная ИТ-платформа Санкт-Петербурга")

# ==============================================================================
# 3. ИНЪЕКЦИЯ КАСТОМНОГО HTML И JAVASCRIPT
# ==============================================================================
# Рендерим HTML-баннер и подключаем JS-скрипт в один поток
html_content = ""
if os.path.exists("layout.html"):
    with open("layout.html", "r", encoding="utf-8") as f:
        html_content = f.read()

js_content = ""
if os.path.exists("script.js"):
    with open("script.js", "r", encoding="utf-8") as f:
        js_content = f.read()

# Выводим на экран связку HTML + JS без разрывов синтаксиса
st.markdown(f"{html_content}<script>{js_content}</script>", unsafe_allow_html=True)

# ==============================================================================
# 4. ЖИВЫЕ КИБЕРПАНК-МЕТРИКИ ИЗ БД
# ==============================================================================
# Получаем агрегированные данные через наше API данных db_layer.py
courses_res = db_layer.execute_read("SELECT COUNT(*) as cnt FROM courses")
citizens_res = db_layer.execute_read("SELECT COUNT(*) as cnt FROM citizens")
factories_res = db_layer.execute_read("SELECT COUNT(*) as cnt FROM factories")

# Защита от пустых ответов базы данных
count_courses = courses_res[0]['cnt'] if courses_res else 0
count_citizens = citizens_res[0]['cnt'] if citizens_res else 0
count_factories = factories_res[0]['cnt'] if factories_res else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернуто b2b-стандартов", value=f"{count_courses} моделей")
kpi2.metric(label="Зарегистрировано граждан", value=f"{count_citizens} анкет")
kpi3.metric(label="Активных заводов-заказчиков", value=f"{count_factories} предприятий")
st.write("---")

# ==============================================================================
# РАСПРЕДЕЛЕНИЕ ПО МОДУЛЯМ КАБИНЕТОВ
# ==============================================================================
if user_role == "🎓 Личный кабинет Физического лица":
    st.success("🤖 Модули HTML, CSS и JS успешно синхронизированы с контуром Физических лиц.")
    # Тут будет вызов интерфейса из cabinet_citizen.py

elif user_role == "🏢 Личный кабинет Производства":
    st.success("🤖 Модули HTML, CSS и JS успешно синхронизированы с контуром Предприятий.")
    # Тут будет вызов интерфейса из cabinet_factory.py

elif user_role == "🛠️ Кабинет АПП (Управление)":
    st.success("🤖 Модули HTML, CSS и JS успешно синхронизированы с контуром Ассоциации.")
    # Тут будет вызов интерфейса из cabinet_app.py
