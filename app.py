import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ================= ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ (SQLite) =================
def init_db():
    conn = sqlite3.connect('prom_quality.db')
    cursor = conn.cursor()
    # Таблица для цифровых следов (Вариант 1)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            target_factory TEXT,
            timestamp TEXT
        )
    ''')
    # Таблица для бронирования оборудования (Вариант 2)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lab_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            hours_requested INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Настройка страницы в строгом стиле B2B
st.set_page_config(page_title="ПромКачество.СПб", layout="wide")

st.title("Экосистема «ПромКачество.СПб»")
st.caption("Прототип концепта для Ассоциации промышленных производств")

# Боковое меню выбора концепции
option = st.sidebar.radio(
    "Выберите вариант концепции для демонстрации:",
    ("Вариант 1: Кадровый хаб (B2B/B2G)", 
     "Вариант 2: Шеринг-экономика & R&D (B2B)", 
     "Вариант 3: Суперапп образования (B2C)",
     "📊 Панель Ассоциации (Просмотр БД)")
)

if option == "Вариант 1: Кадровый хаб (B2B/B2G)":
    st.header("🎯 Концепт: Сквозной цифровой след выпускника")
    st.write("Идея Яндекса: Автоматический мэтчинг кадров под заводы. Контроль качества: Оценка компетенций.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Профиль студента (Политех / ИТМО)")
        st.info("**ФИО:** Иванов Иван Игоревич\n\n**Специализация:** Робототехника и АСУ ТП\n\n**Рейтинг QA:** ⭐️ 4.9 / 5.0 (Верифицировано)")
        st.success("✅ Подтвержденные навыки: Программирование ПЛК, Проектирование в КОМПАС-3D")
    
    with col2:
        st.subheader("Запросы от заводов (Автоматический подбор)")
        st.metric(label="Подходящие вакансии на заводах СПб", value="14 предприятий", delta="3 новых сегодня")
        
        # ЗАПИСЬ В БАЗУ ДАННЫХ ПРИ КЛИКЕ
        if st.button("Передать цифровой след на Кировский завод"):
            conn = sqlite3.connect('prom_quality.db')
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO student_shares (student_name, target_factory, timestamp) VALUES (?, ?, ?)",
                ("Иванов Иван Игоревич", "Кировский завод", now)
            )
            conn.commit()
            conn.close()
            st.toast("Данные успешно сохранены в БД и отправлены в HR-департамент Кировского завода!")

    # ИСПРАВЛЕНО: Синтаксическая ошибка в графике устранена
    st.subheader("📈 Аналитика: Прогноз дефицита инженеров в СПб (тыс. чел.)")
    chart_data = pd.DataFrame({
        "Год":,
        "Дефицит кадров": [4.2, 5.8, 7.5, 9.1]
    }).set_index("Год")
    st.line_chart(chart_data)

elif option == "Вариант 2: Шеринг-экономика & R&D (B2B)":
    st.header("🔬 Концепт: Маркетплейс научных и образовательных услуг")
    st.write("Идея Авито: Объявления о свободных мощностях институтов. Контроль качества: Финансовый арбитраж и SLA.")
    
    tab1, tab2 = st.tabs(["🛒 Доступное оборудование / Услуги", "🤝 Активные контракты (Арбитраж)"])
    
    with tab1:
        st.subheader("Каталог институтов и коммерческих лабораторий")
        st.json({
            "Лаборатория материаловедения (ЦНИИ КМ 'Прометей')": "Испытания металлов на прочность. Доступно: с 15 июня. Цена: 45 000 руб/час.",
            "Кафедра лазерных технологий (ИТМО)": "Лазерная резка и напыление. Доступно: под заказ. Рейтинг выполнения SLA: 98%."
        })
        
        # Интерактивная форма заявки
        st.write("---")
        st.subheader("📝 Быстрое бронирование тайм-слота")
        with st.form("booking_form"):
            company_name = st.text_input("Название вашего предприятия:", placeholder="ООО Завод Арсенал")
            hours = st.number_input("Необходимое количество часов:", min_value=1, max_value=100, value=5)
            submitted = st.form_submit_button("Забронировать")
            
            # ЗАПИСЬ В БАЗУ ДАННЫХ ПРИ ОТПРАВКЕ ФОРМЫ
            if submitted:
                if company_name.strip() == "":
                    st.error("Пожалуйста, введите название предприятия.")
                else:
                    conn = sqlite3.connect('prom_quality.db')
                    cursor = conn.cursor()
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        "INSERT INTO lab_bookings (company_name, hours_requested, timestamp) VALUES (?, ?, ?)",
                        (company_name, hours, now)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"Заявка от {company_name} на {hours} ч. успешно записана в БД! Ожидайте верификации Ассоциацией.")
            
    with tab2:
        st.warning("⚠️ Контроль качества: НИИ 'Вектор' задерживает отчет по ТЗ для завода 'Арсенал'. Рейтинг исполнителя временно снижен на 0.2 балла.")

elif option == "Вариант 3: Суперапп образования (B2C)":
    st.header("🎒 Концепт: Навигатор промышленного образования СПб")
    st.write("Идея Яндекса: Бесшовная покупка путевок и курсов. Контроль качества: Отзывы родителей и аудит условий.")
    
    st.text_input("Поиск образовательной траектории для ребенка:", "Хочу, чтобы ребенок стал инженером авиастроения")
    
    st.subheader("Рекомендованный бесшовный трек:")
    st.markdown("""
    1. **Школа:** Авиастроительный лицей №3 (Рейтинг Ассоциации: ⭐️ 4.8)
    2. **Доп. образование:** Коммерческий ИТ-институт 'Шаг' (Курс '3D-моделирование БПЛА') — *Проверено Отраслевой комиссией*
    3. **Вуз-партнер:** ГУАП (Целевой контракт от ОДК-Климов)
    """)
    
    # Интерактивная карта расположения объектов
    st.subheader("📍 Расположение учебных центров на карте СПб")
    map_data = pd.DataFrame({
        'lat': [59.9342, 59.9284, 59.9722],
        'lon': [30.3351, 30.3204, 30.3012]
    })
    st.map(map_data)
    
    st.button("Записаться на экскурсию на производство")

# ================= СЕКРЕТНАЯ ВКЛАДКА ДЛЯ МОНИТОРИНГА БД =================
elif option == "📊 Панель Ассоциации (Просмотр БД)":
    st.header("📊 Мониторинг базы данных «ПромКачество.СПб»")
    st.write("Здесь Ассоциация в реальном времени видит все b2b-клики и заявки, сохраненные в SQLite.")
    
    conn = sqlite3.connect('prom_quality.db')
    
    st.subheader("1. Логи передачи цифровых следов студентов (Вариант 1)")
    try:
        df_students = pd.read_sql_query("SELECT * FROM student_shares ORDER BY id DESC", conn)
        if not df_students.empty:
            st.dataframe(df_students, use_container_width=True)
        else:
            st.info("В базе данных пока нет логов отправки цифровых следов.")
    except Exception as e:
        st.info("В базе данных пока нет логов отправки цифровых следов.")
        
    st.subheader("2. Заявки на бронирование R&D оборудования (Вариант 2)")
    try:
        df_bookings = pd.read_sql_query("SELECT * FROM lab_bookings ORDER BY id DESC", conn)
        if not df_bookings.empty:
            st.dataframe(df_bookings, use_container_width=True)
        else:
            st.info("В базе данных пока нет active заявок на шеринг оборудования.")
    except Exception as e:
        st.info("В базе данных пока нет active заявок на шеринг оборудования.")
        
    conn.close()
