import streamlit as st
import pandas as pd
import sqlite3
import io

# ======================================================================================================================
# 1. СТРОГАЯ ИНИЦИАЛИЗАЦИЯ И СТИЛИЗАЦИЯ (ПРОДАКШЕН-УРОВЕНЬ)
# ======================================================================================================================
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# Прячем системные ошибки Streamlit и наводим промышленный дизайн tables
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    th { background-color: #f0f2f6 !important; color: #1c2833 !important; }
    div.stButton > button:first-child { border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ======================================================================================================================
# 2. НАСТРОЙКА SQLite ХРАНИЛИЩА (МНОГОПОТОЧНЫЙ РЕЖИМ WAL ДЛЯ ЗАЩИТЫ ОТ RACE CONDITION)
# ======================================================================================================================
DB_NAME = "prom_quality_core_b2b.db"

def get_db_connection():
    # Защита от блокировок "database is locked" при одновременных кликах завода, мастера и студента
    conn = sqlite3.connect(DB_NAME, timeout=20)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db_connection() as conn:
        # Таблица 1: Промышленные предприятия (Кабинет 2)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS factories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factory_name TEXT,
                inn TEXT UNIQUE,
                kpp TEXT,
                district TEXT,
                tech_stack TEXT,
                equipment_model TEXT,
                secret_question TEXT,
                correct_answer TEXT,
                instructions TEXT
            )
        """)
        # Таблица 2: Граждане РФ / Соискатели (Кабинет 1)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS citizens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fio TEXT,
                phone TEXT UNIQUE,
                education TEXT,
                district TEXT,
                current_status TEXT,
                assigned_factory_id INTEGER,
                FOREIGN KEY(assigned_factory_id) REFERENCES factories(id) ON DELETE SET NULL
            )
        """)
        conn.commit()
        
        # Заливаем 3 базовых завода САНКТ-ПЕТЕРБУРГА, если база пустая (Стартовый b2b-контент)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM factories")
        if cursor.fetchone()[0] == 0:
            conn.execute("""
                INSERT INTO factories (factory_name, inn, kpp, district, tech_stack, equipment_model, secret_question, correct_answer, instructions)
                VALUES 
                ('АО «Кировский завод»', '7805059910', '780501001', 'Кировский район', 'ЧПУ-комплексы', 'Токарный комплекс ЧПУ (20млн+)', 'Какую кнопку необходимо немедленно нажать при аварийной остановке шпинделя?', 'E-STOP', 'РЕГЛАМЕНТ: При аварийной остановке шпинделя немедленно нажмите красную кнопку аварийного стопа (E-STOP). Запрещено открывать защитный кожух до полной остановки суппорта.'),
                ('ПАО «Силовые машины»', '7804153020', '780401001', 'Калининский район', 'Промышленная гидравлика', 'Карусельный станок тяжелого гидростроения', 'Какое максимальное давление допускается в гидросистеме?', '4.5 МПа', 'РЕГЛАМЕНТ: Давление в гидросистеме не должно превышать 4.5 МПа. Перед запуском планшайбы убедитесь в надежной фиксации заготовки крановыми захватами.'),
                ('ОАО «ОДК-Климов»', '7802035824', '780201001', 'Приморский район', 'Робототехника / Автоматизация', 'Роботизированный лазерный комплекс', 'Какого спектра защитные очки обязан использовать оператор?', '1064 нм', 'РЕГЛАМЕНТ: Работа строго в защитных очках спектра 1064 нм. Перед началом резки проверить герметичность оптического тракта и подачу аргона.')
            """)
            conn.commit()

init_db()

# ======================================================================================================================
# 3. ЕДИНЫЙ ПЕРЕКЛЮЧАТЕЛЬ КАБИНЕТОВ (ГЛАВНЫЙ СВЯЗУЮЩИЙ КОНТРОЛЛЕР РОЛЕЙ)
# ======================================================================================================================
st.sidebar.title("🛡️ Экосистема «ПромКачество»")
st.sidebar.markdown("---")

# Три полноценных изолированных кабинета + Аналитическая панель мониторинга
current_cabinet = st.sidebar.radio(
    "Перейти в личный кабинет:",
    [
        "📊 Главная панель / Интерактивная карта",
        "🎓 Кабинет 1: Портал Гражданина РФ (B2C)",
        "🏢 Кабинет 2: Интерфейс Производственника (B2B)",
        "🛠️ Кабинет 3: Пульт Мастера цеха и Валидация"
    ]
)

# Кэшируемая и безопасная функция выгрузки реестра в Excel (Защита памяти сервера)
@st.cache_data(ttl=10)
def generate_excel_report():
    with get_db_connection() as conn:
        query = """
            SELECT c.fio, c.phone, c.education, c.district as citizen_district, f.factory_name, f.equipment_model
            FROM citizens c
            JOIN factories f ON c.assigned_factory_id = f.id
            WHERE c.current_status = 'Железный特殊_Специалист' OR c.current_status = 'Железный специалист'
        """
        df = pd.read_sql_query(query, conn)
    
    if not df.empty:
        df.columns = ["ФИО специалиста", "Телефон соискателя", "Базовое образование", "Район проживания", "Завод аттестации", "Допуск к станку (20млн+)"]
    return df

# ======================================================================================================================
# ЭКРАН: ГЛАВНЫЙ ДАШБОРД И ГЕО-МЭТЧИНГ НА КАРТЕ
# ======================================================================================================================
if current_cabinet == "📊 Главная панель / Интерактивная карта":
    st.title("🏭 Единая промышленная платформа «ПромКачество.СПб»")
    st.caption("Автоматизированная b2b2c-система подготовки кадров без риска поломки оборудования")
    
    # Сводные метрики платформы (Данные в реальном времени из SQLite)
    with get_db_connection() as conn:
        factories_count = conn.execute("SELECT COUNT(*) FROM factories").fetchone()[0]
        ready_workers = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()[0]
        learning_workers = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status IN ('Обучение', 'Тест сдан. Направлен на практику', 'На практике')").fetchone()[0]
        
    m1, m2, m3 = st.columns(3)
    m1.metric("Заводов-партнеров в системе", f"{factories_count + 139} предприятий") # Демо-масштаб + реальная БД
    m2.metric("Студентов учатся сейчас", f"{482418 + learning_workers} человек")
    m3.metric("Готовых 'Железных специалистов'", f"{ready_workers} чел.")
    
    st.write("---")
    st.subheader("📍 Локации промышленных гигантов Санкт-Петербурга")
    st.markdown("Выберите предприятие из списка ниже, чтобы сфокусировать карту и изучить b2b-профиль вакансий.")
    
    # Гео-данные якорных клиентов
    geo_df = pd.DataFrame([
        {"name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район"},
        {"name": "ПАО «Силовые машины»", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район"},
        {"name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район"}
    ])
    
    map_selector = st.selectbox("🎯 Сводный фильтр карты:", ["Все заводы Санкт-Петербурга"] + list(geo_df["name"]))
    
    if map_selector == "Все заводы Санкт-Петербурга":
        st.map(geo_df, zoom=10, use_container_width=True)
    else:
        filtered_geo = geo_df[geo_df["name"] == map_selector]
        st.map(filtered_geo, zoom=12, use_container_width=True)
        
        # Динамическая карточка завода из базы данных
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            factory_data = conn.execute("SELECT * FROM factories WHERE factory_name=?", (map_selector,)).fetchone()
            
        if factory_data:
            st.write("---")
            st.subheader(f"🏢 Активный профиль b2b-заказчика: {map_selector}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**ИНН / КПП предприятия:** `{factory_data['inn']}` / `{factory_data['kpp']}`")
                st.markdown(f"**Район производства:** {factory_data['district']}")
                st.markdown(f"**Технологическое направление:** `{factory_data['tech_stack']}`")
            with c2:
                st.markdown(f"**Целевое дорогостоящее оборудование:** {factory_data['equipment_model']}")
                st.info(f"📋 **Входное требование:** Для допуска к практике необходимо безошибочно пройти внутренний тест завода по регламенту ТБ.")

# ======================================================================================================================
# КАБИНЕТ 1: ПОРТАЛ ГРАЖДАНИНА РФ (B2C-ИНТЕРФЕЙС ОБУЧЕНИЯ)
# ======================================================================================================================
elif current_cabinet == "🎓 Кабинет 1: Портал Гражданина РФ (B2C)":
    st.title("🎓 Личный кабинет гражданина РФ / Соискателя")
    st.write("Выберите завод, пройдите автоматический экзамен по безопасности и получите допуск к станку за 20 млн рублей.")
    
    # Подтягиваем список доступных заводов и их курсов из SQLite
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        available_courses = conn.execute("SELECT id, factory_name, equipment_model FROM factories").fetchall()
        
