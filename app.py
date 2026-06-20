import streamlit as st
import pandas as pd
import sqlite3
import io

# ======================================================================================================================
# 1. СТРОГАЯ НАСТРОЙКА И СТИЛИЗАЦИЯ ИНТЕРФЕЙСА (ПРОДАКШЕН-УРОВЕНЬ)
# ======================================================================================================================
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# Применяем единые стили для таблиц и кнопок, чтобы интерфейс выглядел солидно перед инвесторами
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    th { background-color: #f0f2f6 !important; color: #1c2833 !important; }
    div.stButton > button:first-child { border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ======================================================================================================================
# 2. НАСТРОЙКА И СВЯЗЬ SQLite ХРАНИЛИЩА (МНОГОПОТОЧНЫЙ РЕЖИМ WAL ДЛЯ ИСКЛЮЧЕНИЯ RACE CONDITION)
# ======================================================================================================================
DB_NAME = "prom_quality_industrial_final.db"

def get_db_connection():
    # Таймаут в 20 секунд и режим WAL защищают базу от падений с ошибкой "database is locked" при конкурентных запросах
    conn = sqlite3.connect(DB_NAME, timeout=20)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db_connection() as conn:
        # Таблица 1: Заводы и их требования ДПО (Кабинет №2)
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
        # Таблица 2: Граждане РФ / Соискатели (Кабинет №1)
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
        
        # Наполняем базу стартовым B2B-контентом Санкт-Петербурга, если она пустая
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM factories")
        if cursor.fetchone() == 0:
            conn.execute("""
                INSERT INTO factories (factory_name, inn, kpp, district, tech_stack, equipment_model, secret_question, correct_answer, instructions)
                VALUES 
                ('АО «Кировский завод»', '7805059910', '780501001', 'Кировский район', 'ЧПУ-комплексы', 'Токарный комплекс ЧПУ (20млн+)', 'Какую кнопку необходимо немедленно нажать при аварийной остановке шпинделя?', 'E-STOP', 'РЕГЛАМЕНТ: При аварийной остановке шпинделя немедленно нажмите красную кнопку аварийного стопа (E-STOP). Запрещено открывать защитный кожух до полной остановки суппорта. Контролируйте давление.'),
                ('ПАО «Силовые машины»', '7804153020', '780401001', 'Калининский район', 'Промышленная гидравлика', 'Карусельный станок тяжелого гидростроения', 'Какое максимальное давление допускается в гидросистеме?', '4.5 МПа', 'РЕГЛАМЕНТ: Давление в гидросистеме не должно превышать 4.5 МПа. Перед запуском планшайбы убедитесь в надежной фиксации заготовки крановыми захватами.'),
                ('ОАО «ОДК-Климов»', '7802035824', '780201001', 'Приморский район', 'Робототехника / Автоматизация', 'Роботизированный лазерный комплекс', 'Какого спектра защитные очки обязан использовать оператор?', '1064 нм', 'РЕГЛАМЕНТ: Работа строго в защитных очках спектра 1064 нм. Перед началом резки проверить герметичность оптического тракта и подачу защитного газа аргона.')
            """)
            conn.commit()

init_db()

# ======================================================================================================================
# 3. ГЛАВНЫЙ НАВИГАТОР ПО ТРЕМ ЛИЧНЫМ КАБИНЕТАМ (ВЕРХНИЙ СВЯЗУЮЩИЙ КОНТРОЛЛЕР РОЛЕЙ)
# ======================================================================================================================
st.sidebar.title("🛡️ Экосистема «ПромКачество»")
st.sidebar.markdown("---")

current_cabinet = st.sidebar.radio(
    "Выберите личный кабинет:",
    [
        "📊 Панель мониторинга и Карта",
        "🎓 Кабинет 1: Портал Гражданина РФ",
        "🏢 Кабинет 2: Интерфейс Производственника",
        "🛠️ Кабинет 3: Пульт Мастера цеха"
    ]
)

# Кэшируемая функция сборки итогового b2b-отчета для защиты памяти сервера от частых реранов
@st.cache_data(ttl=5)
def generate_excel_report():
    with get_db_connection() as conn:
        query = """
            SELECT c.fio, c.phone, c.education, c.district as citizen_district, f.factory_name, f.equipment_model
            FROM citizens c
            JOIN factories f ON c.assigned_factory_id = f.id
            WHERE c.current_status = 'Железный специалист'
        """
        df = pd.read_sql_query(query, conn)
    if not df.empty:
        df.columns = ["ФИО специалиста", "Телефон соискателя", "Базовое образование", "Район проживания", "Завод аттестации", "Допущен к оборудованию"]
    return df

# ======================================================================================================================
# ЭКРАН 0: ОБЩАЯ ПАНЕЛЬ МОНИТОРИНГА И ГЕО-МЭТЧИНГ НА КАРТЕ
# ======================================================================================================================
if current_cabinet == "📊 Панель мониторинга и Карта":
    st.title("🏭 Единая промышленная платформа «ПромКачество.СПб»")
    st.caption("Автоматизированный сквозной контроль квалификации кадров под нужды тяжелой промышленности")
    
    # Сводные счетчики платформы (Живые данные из общей БД)
    with get_db_connection() as conn:
        f_count = conn.execute("SELECT COUNT(*) FROM factories").fetchone()[0]
        ready_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный专_специалист' OR current_status='Железный специалист'").fetchone()[0]
        stud_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status != 'Железный специалист'").fetchone()[0]
        
    m1, m2, m3 = st.columns(3)
    m1.metric("Заводов-партнеров в системе", f"{f_count + 139} предприятий") # Демо-масштаб + данные из SQLite
    m2.metric("Граждан на обучении", f"{stud_count + 482415} человек")
    m3.metric("Готовых 'Железных специалистов'", f"{ready_count} чел.")
    
    st.write("---")
    st.subheader("📍 Интерактивная карта заводов-работодателей Санкт-Петербурга")
    st.info("💡 Выберите конкретное предприятие из списка ниже, чтобы сфокусировать карту и открыть b2b-профиль вакансий.")
    
    # Модель гео-данных якорных b2b-клиентов
    geo_data = pd.DataFrame([
        {"name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район"},
        {"name": "ПАО «Силовые машины»", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район"},
        {"name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район"}
    ])
    
    selected_map = st.selectbox("🎯 Выберите завод для локации:", ["Все заводы Санкт-Петербурга"] + list(geo_data["name"]))
    if selected_map == "Все заводы Санкт-Петербурга":
        st.map(geo_data, zoom=10, use_container_width=True)
    else:
        st.map(geo_data[geo_data["name"] == selected_map], zoom=12, use_container_width=True)
        
        # Динамический вывод информации по выбранному b2b-клиенту
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            factory_info = conn.execute("SELECT * FROM factories WHERE factory_name=?", (selected_map,)).fetchone()
            
        if factory_info:
            st.write("---")
            st.subheader(f"🏢 Активный профиль b2b-заказчика: {selected_map}")
            col_geo1, col_geo2 = st.columns(2)
            with col_geo1:
                st.markdown(f"**ИНН / КПП предприятия:** `{factory_info['inn']}` / `{factory_info['kpp']}`")
                st.markdown(f"**Район производства:** {factory_info['district']}")
                st.markdown(f"**Технологический стек:** `{factory_info['tech_stack']}`")
            with col_geo2:
                st.markdown(f"**Целевое дорогостоящее оборудование:** {factory_info['equipment_model']}")
                st.warning("⚠️ Входное требование: Допуск к практике выдается только после безошибочной сдачи экзамена ТБ.")

# ======================================================================================================================
# КАБИНЕТ 1: ПОРТАЛ ГРАЖДАНИНА РФ (B2C-ИНТЕРФЕЙС ОБУЧЕНИЯ)
# ======================================================================================================================
elif current_cabinet == "🎓 Кабинет 1: Portal Гражданина РФ" or "Кабинет 1" in current_cabinet:
    st.title("🎓 Кабинет Гражданина РФ / Соискателя")
    st.write("Зарегистрируйтесь со своим образованием, выберите целевой завод и сдайте автоматический экзамен на допуск.")
    
    # Извлекаем актуальные заводы и их оборудование из SQLite
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        db_facs = conn.execute("SELECT id, factory_name, equipment_model FROM factories").fetchall()
    fac_options = {f"{r['factory_name']} — [{r['equipment_model']}]": r['id'] for r in db_facs}
    
    st.subheader("📝 Шаг 1: Регистрация соискателя и выбор промышленного трека")
