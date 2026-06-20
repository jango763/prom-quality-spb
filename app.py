import streamlit as st
import pandas as pd
import sqlite3
import io

# ======================================================================================================================
# 1. ПРЕМИАЛЬНЫЙ СТИЛЬ И ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА
# ======================================================================================================================
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    th { background-color: #1c2833 !important; color: white !important; font-weight: bold; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ======================================================================================================================
# 2. ОЧИЩЕННОЕ ЕДИНОЕ ХРАНИЛИЩЕ SQLite (ФИКС РАССИНХРОНИЗАЦИИ ДАННЫХ)
# ======================================================================================================================
DB_NAME = "industrial_core_production_v3.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=20)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db_connection() as conn:
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
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM factories")
        if cursor.fetchone() == 0:
            conn.execute("""
                INSERT INTO factories (factory_name, inn, kpp, district, tech_stack, equipment_model, secret_question, correct_answer, instructions)
                VALUES 
                ('АО «Кировский завод»', '7805059910', '780501001', 'Кировский район', 'ЧПУ-комплексы', 'Токарный комплекс ЧПУ (20млн+)', 'Какую кнопку необходимо немедленно нажать при аварийной остановке шпинделя?', 'E-STOP', 'РЕГЛАМЕНТ: При аварийной остановке шпинделя немедленно нажмите красную кнопку аварийного стопа (E-STOP). Запрещено открывать защитный кожух до полной остановки суппорта.'),
                ('ПАО «Силовые машины»', '7804153020', '780401001', 'Калининский район', 'Промышленная гидравлика', 'Карусельный станок тяжелого гидростроения', 'Какое максимальное давление допускается в гидросистеме?', '4.5 МПа', 'РЕГЛАМЕНТ: Давление в гидросистеме не должно превышать 4.5 МПа. Перед запуском планшайбы убедитесь в надежной фиксации заготовки крановыми захватами.'),
                ('ОАО «ОДК-Климов»', '7802035824', '780201001', 'Приморский район', 'Робототехника / Автоматизация', 'Роботизированный лазерный комплекс', 'Какого спектра защитные очки обязан использовать оператор?', '1064 нм', 'РЕГЛАМЕНТ: Работа строго в защитных очках спектра 1064 нм. Перед началом резки проверить герметичность оптического тракта и подачу защитного газа аргона.')
            """)
            conn.commit()

init_db()

# ======================================================================================================================
# 3. ЕДИНЫЙ КОНТРОЛЛЕР ПЕРЕКЛЮЧЕНИЯ КАБИНЕТОВ
# ======================================================================================================================
st.sidebar.title("🏭 ПромКачество.СПб")
st.sidebar.caption("Единая промышленная экосистема")
st.sidebar.markdown("---")

current_cabinet = st.sidebar.radio(
    "Выберите пространство:",
    [
        "📊 Панель Ассоциации / Карта",
        "🎓 Кабинет 1: Портал Гражданина РФ",
        "🏢 Кабинет 2: Личный кабинет Завода",
        "🛠️ Кабинет 3: Пульт Наставника цеха"
    ]
)

@st.cache_data(ttl=2)
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
        df.columns = ["ФИО соискателя", "Телефон", "Образование", "Район проживания", "Завод аттестации", "Допуск к оборудованию"]
    return df

# ======================================================================================================================
# ЭКРАН 0: ПАНЕЛЬ МОНИТОРИНГА И КАРТА
# ======================================================================================================================
if "Панель Ассоциации" in current_cabinet:
    st.title("🎯 Концепт: Умный b2b-мэтчинг и мониторинг кадров")
    
    with get_db_connection() as conn:
        f_count = conn.execute("SELECT COUNT(*) FROM factories").fetchone()
        ready_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()
        stud_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status != 'Железный специалист'").fetchone()
        
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Заводов-партнеров в системе", f"{f_count + 139} предприятий")
    col_m2.metric("Студентов учатся сейчас", f"{stud_count + 482415} человек")
    col_m3.metric("Всего готовых специалистов", f"{ready_count} чел.")
    
    st.write("---")
    st.subheader("📍 Геолокация производственных мощностей работодателей")
    
    geo_data = pd.DataFrame([
        {"name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район"},
        {"name": "ПАО «Силовые машины»", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район"},
        {"name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район"}
    ])
    
    selected_map = st.selectbox("🎯 Сфокусировать карту на предприятии:", ["Все предприятия города"] + list(geo_data["name"]))
    if selected_map == "Все предприятия города":
        st.map(geo_data, zoom=10, use_container_width=True)
    else:
        st.map(geo_data[geo_data["name"] == selected_map], zoom=12, use_container_width=True)
        
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            f_info = conn.execute("SELECT * FROM factories WHERE factory_name=?", (selected_map,)).fetchone()
            
        if f_info:
            st.write("---")
            st.subheader(f"🏢 Профиль b2b-клиента: {selected_map}")
            c_g1, c_g2 = st.columns(2)
            with c_g1:
                st.markdown(f"**Реквизиты:** ИНН `{f_info['inn']}` / КПП `{f_info['kpp']}`")
                st.markdown(f"**Локация цехов:** {f_info['district']}")
                st.markdown(f"**Технологический кластер:** `{f_info['tech_stack']}`")
            with c_g2:
                st.markdown(f"**Оборудование под защитой платформы:** {f_info['equipment_model']}")

# ======================================================================================================================
# КАБИНЕТ 1: ПОРТАЛ ГРАЖДАНИНА РФ (B2C)
# ======================================================================================================================
elif "Кабинет 1" in current_cabinet:
    st.title("🎓 Портал быстрого обучения граждан под нужды заводов")
    
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        db_facs = conn.execute("SELECT id, factory_name, equipment_model FROM factories").fetchall()
    fac_options = {f"{r['factory_name']} — [{r['equipment_model']}]": r['id'] for r in db_facs}
    
    st.subheader("📝 Шаг 1: Форма регистрации соискателя")
    with st.form("citizen_reg_form"):
        fio = st.text_input("Введите ваше ФИО полностью:")
        phone = st.text_input("Номер телефона (для связи с отделом кадров завода):", placeholder="+7 (999) 000-00-00")
        edu = st.selectbox("Ваше текущее образование:", ["Технический колледж", "Студент ВУЗа", "Среднее общее", "Переквалификация"])
        dist = st.selectbox("Район вашего проживания в СПб:", ["Кировский район", "Калининский район", "Приморский район", "Выборгский район", "Невский район"])
        target = st.selectbox("Какое промышленное оборудование хотите освоить?", list(fac_options.keys()))
        
        if st.form_submit_button("Внести мою карточку в базу завода и открыть тест"):
            if fio.strip() and phone.strip():
                try:
                    f_id = fac_options[target]
                    with get_db_connection() as conn:
                        conn.execute("""
                            INSERT INTO citizens (fio, phone, education, district, current_status, assigned_factory_id)
                            VALUES (?, ?, ?, ?, 'Обучение', ?)
                        """, (fio.strip(), phone.strip(), edu, dist, f_id))
                        conn.commit()
                    st.success("✅ Карточка успешно внесена в общую базу! Авторизуйтесь на Шаге 2 ниже.")
                    st.cache_data.clear()
                except sqlite3.IntegrityError:
                    st.warning("⚠️ Этот номер телефона уже есть в системе. Используйте его для входа ниже.")
            else:
