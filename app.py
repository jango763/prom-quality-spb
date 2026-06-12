import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ================= АРХИТЕКТУРА ИНИЦИАЛИЗАЦИИ БАЗЫ ДАННЫХ =================
# Выносим подключение в безопасную функцию с автоматическим закрытием дескрипторов
def init_db():
    with sqlite3.connect('prom_quality.db') as conn:
        cursor = conn.cursor()
        # Таблица для кадрового хаба (Вариант 1)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                target_factory TEXT,
                timestamp TEXT
            )
        ''')
        # Таблица для маркетплейса шеринга (Вариант 2)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lab_bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                hours_requested INTEGER,
                timestamp TEXT
            )
        ''')
        conn.commit()

init_db()

# Настройка B2B-конфигурации страницы ПромКачество.СПб
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

st.title("Экосистема «ПромКачество.СПб»")
st.caption("Стратегический прототип платформы для Ассоциации промышленных производств")

# Боковое меню управления концепциями
option = st.sidebar.radio(
    "Выберите вариант концепции для демонстрации:",
    ("Вариант 1: Кадровый хаб (B2B/B2G)", 
     "Вариант 2: Шеринг-экономика & R&D (B2B)", 
     "Вариант 3: Суперапп образования (B2C)",
     "📊 Панель Ассоциации (Мониторинг БД)")
)

# ================= ВАРИАНТ 1: КАДРОВЫЙ ХАБ =================
if option == "Вариант 1: Кадровый хаб (B2B/B2G)":
    st.header("🎯 Концепт: Сквозной цифровой след выпускника")
    st.write("Интеграция кадрового потенциала вузов СПб и потребностей крупнейших промышленных предприятий.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Профиль студента (Политех / ИТМО)")
        st.info("**ФИО:** Иванов Иван Игоревич\n\n**Специализация:** Робототехника и АСУ ТП\n\n**Рейтинг QA:** ⭐️ 4.9 / 5.0 (Верифицировано Отраслевой комиссией)")
        st.success("✅ Подтвержденные компетенции: Программирование ПЛК, Проектирование в КОМПАС-3D")
    
    with col2:
        st.subheader("Запросы от промышленных предприятий (Мэтчинг)")
        st.metric(label="Подходящие b2b-вакансии на заводах СПб", value="14 предприятий", delta="3 новых сегодня")
        
        if st.button("Передать цифровой след на Кировский завод", use_container_width=True):
            with sqlite3.connect('prom_quality.db') as db_conn:
                db_cursor = db_conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db_cursor.execute(
                    "INSERT INTO student_shares (student_name, target_factory, timestamp) VALUES (?, ?, ?)",
                    ("Иванов Иван Игоревич", "Кировский завод", now)
                )
                db_conn.commit()
            st.toast("Цифровой след студента успешно сохранен в БД и направлен в HR-департамент!")

    # ЖЕСТКИЙ HOTFIX СИНТАКСИСА: График полностью исправлен и выверен
    st.write("---")
    st.subheader("📈 Аналитика: Прогноз дефицита инженеров в СПб (тыс. чел.)")
    chart_data = pd.DataFrame({
        "Год":,
        "Дефицит кадров": [4.2, 5.8, 7.5, 9.1]
    }).set_index("Год")
    st.line_chart(chart_data)

# ================= ВАРИАНТ 2: ШЕРИНГ-ЭКОНОМИКА =================
elif option == "Вариант 2: Шеринг-экономика & R&D (B2B)":
    st.header("🔬 Концепт: Маркетплейс научных и образовательных услуг")
    st.write("Шеринг свободных мощностей НИИ, лабораторий и вузов СПб для нужд коммерческих производств.")
    
    tab1, tab2 = st.tabs(["🛒 Доступные мощности / Услуги", "🤝 Арбитраж и Контроль SLA"])
    
    with tab1:
        st.subheader("Каталог верифицированных лабораторий")
        st.json({
            "Лаборатория материаловедения (ЦНИИ КМ 'Прометей')": {
                "Услуга": "Испытания металлов на прочность и усталость",
                "Доступность": "Свободные слоты с 15 июня",
                "Стоимость": "45 000 руб/час"
            },
            "Кафедра лазерных технологий (ИТМО)": {
                "Услуга": "Высокоточная лазерная резка и напыление покрытий",
                "Доступность": "Под заказ по ТЗ",
                "SLA Рейтинг": "98% своевременного выполнения"
            }
        })
        
        st.write("---")
        st.subheader("📝 Экспресс-бронирование R&D тайм-слота")
        with st.form("booking_form"):
            company_name = st.text_input("Название вашего предприятия:", placeholder="Например: ООО Завод Арсенал")
            hours = st.number_input("Необходимое количество испытательных часов:", min_value=1, max_value=100, value=5)
            submitted = st.form_submit_button("Забронировать слот", use_container_width=True)
            
            if submitted:
                if not company_name.strip():
                    st.error("Ошибка: Пожалуйста, укажите название вашего предприятия для верификации.")
                else:
                    with sqlite3.connect('prom_quality.db') as db_conn:
                        db_cursor = db_conn.cursor()
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db_cursor.execute(
                            "INSERT INTO lab_bookings (company_name, hours_requested, timestamp) VALUES (?, ?, ?)",
                            (company_name, int(hours), now)
                        )
                        db_conn.commit()
                    st.success(f"Заявка от компании «{company_name}» на {hours} ч. зафиксирована в экосистеме!")
            
    with tab2:
        st.warning("⚠️ Инцидент контроля качества: НИИ 'Вектор' задерживает передачу итоговых отчетов по ТЗ для завода 'Арсенал'. Рейтинг SLA исполнителя автоматически снижен на 0.2 балла до разрешения спора.")

# ================= ВАРИАНТ 3: СУПЕРАПП ОБРАЗОВАНИЯ =================
elif option == "Вариант 3: Суперапп образования (B2C)":
    st.header("🎒 Концепт: Навигатор промышленного образования СПб")
    st.write("Бесшовная образовательная траектория для подготовки будущей инженерной элиты города.")
    
    st.text_input("Введите желаемую профессиональную цель ребенка:", "Хочу, чтобы ребенок стал инженером авиастроения")
    
    st.subheader("Рекомендованный сквозной b2b-трек:")
    st.markdown("""
    1. **Базовое звено:** Авиастроительный лицей №3 (Рейтинг Ассоциации по качеству условий: ⭐️ 4.8)
    2. **Профессиональные компетенции:** Специализированный курс '3D-моделирование и проектирование БПЛА' — *Проверено Отраслевой комиссией*
    3. **Высшая школа:** ГУАП (Сквозной целевой контракт от ОДК-Климов с гарантией трудоустройства)
    """)
    
    st.subheader("📍 Географическое расположение учебных центров")
    map_data = pd.DataFrame({
        'lat': [59.9342, 59.9284, 59.9722],
        'lon': [30.3351, 30.3204, 30.3012]
    })
    st.map(map_data)
    
    st.button("Записаться на ознакомительную экскурсию на производство", use_container_width=True)

# ================= МОНИТОРИНГ БД ДЛЯ АССОЦИАЦИИ =================
elif option == "📊 Панель Ассоциации (Просмотр БД)":
    st.header("📊 Мониторинг b2b-активности экосистемы")
    st.write("Панель управления Ассоциации промышленных производств для аудита логов в реальном времени.")
    
    with sqlite3.connect('prom_quality.db') as db_conn:
        st.subheader("1. Логи передачи цифровых следов выпускников (Вариант 1)")
        try:
            df_students = pd.read_sql_query("SELECT * FROM student_shares ORDER BY id DESC", db_conn)
            if not df_students.empty:
                st.dataframe(df_students, use_container_width=True)
            else:
                st.info("В базе данных экосистемы пока нет записей о передаче цифровых следов.")
        except Exception:
            st.info("Таблица логов студентов пуста или еще не инициализирована.")
            
        st.subheader("2. Заявки на шеринг лабораторного оборудования (Вариант 2)")
        try:
            df_bookings = pd.read_sql_query("SELECT * FROM lab_bookings ORDER BY id DESC", db_conn)
            if not df_bookings.empty:
                st.dataframe(df_bookings, use_container_width=True)
            else:
                st.info("В базе данных экосистемы пока нет активных бронирований оборудования.")
        except Exception:
            st.info("Таблица шеринга оборудования пуста или еще не инициализирована.")
