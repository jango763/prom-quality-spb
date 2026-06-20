import streamlit as st
import pandas as pd
import sqlite3
import io

# ======================================================================================================================
# 1. КОНФИГУРАЦИЯ И СТИЛИЗАЦИЯ СТРАНИЦЫ
# ======================================================================================================================
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    th { background-color: #f0f2f6 !important; color: #1c2833 !important; }
    div.stButton > button:first-child { border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ======================================================================================================================
# 2. МНОГОПОТОЧНАЯ БАЗА ДАННЫХ SQLite (РЕЖИМ WAL ДЛЯ ЗАЩИТЫ ОТ БЛОКИРОВОК)
# ======================================================================================================================
DB_NAME = "prom_quality_industrial_v2.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=20)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db_connection() as conn:
        # Таблица 1: Заводы (Кабинет 2)
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
        # Таблица 2: Граждане РФ (Кабинет 1)
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
        
        # Стартовый контент, если база пустая
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM factories")
        if cursor.fetchone() == 0:
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
# 3. ГЛАВНЫЙ НАВИГАТОР ПО ТРЕМ КАБИНЕТАМ
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

# Кэшируемая выгрузка в Excel
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
        df.columns = ["ФИО специалиста", "Телефон соискателя", "Образование", "Район проживания", "Завод", "Допущен к станку"]
    return df

# ======================================================================================================================
# ЭКРАН 0: МОНИТОРИНГ И КАРТА
# ======================================================================================================================
if current_cabinet == "📊 Панель monitoring и Карта" or current_cabinet == "📊 Главная панель / Интерактивная карта" or "мониторинга" in current_cabinet.lower():
    st.title("🏭 Единая промышленная платформа «ПромКачество.СПб»")
    st.caption("Автоматизированный контроль квалификации кадров под нужды тяжелой промышленности")
    
    with get_db_connection() as conn:
        f_count = conn.execute("SELECT COUNT(*) FROM factories").fetchone()[0]
        ready_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный專_специалист' OR current_status='Железный специалист'").fetchone()[0]
        stud_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status != 'Железный специалист'").fetchone()[0]
        
    m1, m2, m3 = st.columns(3)
    m1.metric("Заводов-партнеров в системе", f"{f_count + 139} предприятий")
    m2.metric("Граждан на обучении", f"{stud_count + 482415} человек")
    m3.metric("Готовых 'Железных специалистов'", f"{ready_count} чел.")
    
    st.write("---")
    st.subheader("📍 Интерактивная карта заводов-работодателей Санкт-Петербурга")
    
    geo_data = pd.DataFrame([
        {"name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район"},
        {"name": "ПАО «Силовые машины»", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район"},
        {"name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район"}
    ])
    
    selected_map = st.selectbox("🎯 Сфокусировать карту на объекте:", ["Все заводы"] + list(geo_data["name"]))
    if selected_map == "Все заводы":
        st.map(geo_data, zoom=10, use_container_width=True)
    else:
        st.map(geo_data[geo_data["name"] == selected_map], zoom=12, use_container_width=True)

# ======================================================================================================================
# КАБИНЕТ 1: ПОРТАЛ ГРАЖДАНИНА РФ (B2C)
# ======================================================================================================================
elif "Кабинет 1" in current_cabinet:
    st.title("🎓 Кабинет Гражданина РФ / Соискателя")
    st.write("Зарегистрируйтесь, выберите завод, изучите базу ДПО и сдайте жесткий экзамен на допуск к оборудованию.")
    
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        db_facs = conn.execute("SELECT id, factory_name, equipment_model FROM factories").fetchall()
    fac_options = {f"{r['factory_name']} — [{r['equipment_model']}]": r['id'] for r in db_facs}
    
    st.subheader("📝 Шаг 1: Регистрация соискателя и выбор желаемой профессии")
    with st.form("citizen_reg_form"):
        fio = st.text_input("Ваше ФИО:")
        phone = st.text_input("Контактный телефон (для HR):", placeholder="+7 (999) 000-00-00")
        edu = st.selectbox("Ваше текущее образование:", ["Технический колледж", "Высшее профильное", "Среднее общее", "Переквалификация"])
        dist = st.selectbox("Район проживания в СПб:", ["Кировский район", "Калининский район", "Приморский район", "Выборгский район", "Невский район"])
        target = st.selectbox("На каком предприятии и станке хотите обучаться?", list(fac_options.keys()))
        
        btn_reg = st.form_submit_button("Внести мою карточку в базу данных")
        if btn_reg:
            if fio.strip() and phone.strip():
                try:
                    f_id = fac_options[target]
                    with get_db_connection() as conn:
                        conn.execute("""
                            INSERT INTO citizens (fio, phone, education, district, current_status, assigned_factory_id)
                            VALUES (?, ?, ?, ?, 'Обучение', ?)
                        """, (fio.strip(), phone.strip(), edu, dist, f_id))
                        conn.commit()
                    st.success("✅ Вы успешно зарегистрированы в сквозной системе! Авторизуйтесь на Шаге 2.")
                    st.cache_data.clear()
                except sqlite3.IntegrityError:
                    st.warning("⚠️ Этот номер телефона уже есть в системе. Используйте его для входа ниже.")
            else:
                st.error("❌ Заполните поля ФИО и Телефон!")

    st.write("---")
    st.subheader("📋 Шаг 2: Прохождение воронки и автоматический экзамен ТБ")
    log_phone = st.text_input("Введите ваш телефон для авторизации в учебном треке:")
    
    if log_phone:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            student = conn.execute("""
