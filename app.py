import streamlit as st
import pandas as pd
import sqlite3
import io

# ==============================================================================
# 1. СТИЛИ ИЗ ВАШЕГО CODEPEN ( Glassmorphism, Киберпанк-неон, Фон #0B0F19 )
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Система Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        /* Полное переопределение фона под тему вашего CodePen */
        .stApp {
            background-color: #0B0F19 !important;
            color: #F8FAFC !important;
        }
        
        /* Наш особый премиум Hero-баннер АПП */
        .hero-banner {
            background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important;
            padding: 35px;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 25px;
            border-left: 8px solid #10B981;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
        }
        .hero-title {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(90deg, #10B981, #34D399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 14px;
            color: #94A3B8;
            margin-top: 8px;
            line-height: 1.4;
        }

        /* Интерактивные матовые B2B-контейнеры (Glassmorphism) */
        div[data-testid="stForm"], div[data-testid="stExpander"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 14px !important;
            padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px);
        }

        /* Объемные b2b-карточки KPI из CodePen */
        .glass-card {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .card-title {
            font-size: 12px;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .card-value {
            font-size: 24px;
            font-weight: 800;
            color: #10B981;
            margin-top: 5px;
        }

        /* Тарифные коробки */
        .tariff-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            margin-bottom: 15px;
        }
        .tariff-box.popular {
            border-color: #10B981;
            background: rgba(16, 185, 129, 0.02);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.05);
        }
        .price {
            font-size: 36px;
            font-weight: 900;
            color: #10B981;
            margin: 10px 0;
        }
        .desc {
            font-size: 13px;
            color: #94A3B8;
        }

        /* Поля ввода */
        .stTextInput input, .stTextArea textarea, .stSelectbox div {
            background-color: rgba(15, 23, 42, 0.6) !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* Вкладки навигации */
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #10B981 !important; border-bottom-color: #10B981 !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ SQLITE (WAL)
# ==============================================================================
DB_NAME = "production_control_enterprise_final_v1.db"

@st.cache_resource
def get_db_connection():
    """Кэшируем подключение к СУБД для максимальной b2b-скорости платформы"""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    """Инициализация таблиц базы данных с идеальным выравниванием отступов"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT, phone TEXT, email TEXT, education TEXT,
            passport TEXT, diploma TEXT, workbook TEXT, skills TEXT,
            gdpr INTEGER DEFAULT 0, score INTEGER DEFAULT 0, status TEXT DEFAULT 'Обучение'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inn TEXT, title TEXT, model TEXT, text TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tariff TEXT, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM citizens")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO citizens (fio, phone, email, education, current_status) VALUES ('Никифоров Артур Владимирович', '+7(921)555-44-33', 'artur@mail.ru', 'Высшее техническое', 'Железный специалист')")
        cursor.execute("INSERT INTO payments (tariff, amount) VALUES ('Безлимитный Год', 150000.0)")
        
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# 3. НАВИГАЦИЯ АПП (Сайдбар и Роли из CodePen)
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#10B981; font-weight:800; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3);'>🔒 КОНТУР АПП</h2>", unsafe_allow_html=True)
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        [
            "🎓 Личный кабинет Физического лица", 
            "🏢 Личный кабинет Производства", 
            "🛠️ Кабинет Ассоциации (Управление)"
        ]
    )
    st.write("---")
    st.caption("ПромКачество.СПб v2.0")

# Вывод премиум Hero-баннера АПП
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
    </div>
""", unsafe_allow_html=True)

# Считываем живую статистику для шапки
conn = sqlite3.connect(DB_NAME)
citizens_df = pd.read_sql_query("SELECT * FROM citizens", conn)
payments_df = pd.read_sql_query("SELECT * FROM payments", conn)
courses_df = pd.read_sql_query("SELECT * FROM courses", conn)
conn.close()

# ==============================================================================
# КАБИНЕТ №1: ГРАЖДАНЕ РФ
# ==============================================================================
if user_role == "🎓 Личный кабинет Физического лица":
    st.markdown("<h3>🎓 Портал обучения и Паспорт Навыков</h3>", unsafe_allow_html=True)
    
    with st.form("citizen_form", clear_on_submit=False):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>📝 Профильная анкетa и загрузка документов</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        c_fio = col1.text_input("ФИО соискателя полностью:", value="Иванов Игорь Игоревич")
        c_phone = col2.text_input("Номер телефона для связи:", value="+7(900)111-22-33")
        c_email = col3.text_input("E-mail соискателя:", value="ivanov@spb.ru")
        
        col4, col5, col6 = st.columns(3)
        c_pass = col4.text_input("Паспорт (Серия, Номер):", placeholder="4011 123456")
        c_diploma = col5.text_input("Диплом (Серия, Номер):", placeholder="№78-01")
        c_work = col6.text_input("Трудовая книжка (Номер):", placeholder="№ТК-99")
        
        c_skills = st.text_area("Расскажите о ваших навыках и опыте работы (анкета о себе):")
        c_gdpr = st.checkbox("Согласие на обработку персональных данных граждан РФ", value=True)
        
        if st.form_submit_button("Сохранить анкету соискателя", type="primary"):
            if c_fio.strip() and c_phone.strip():
                conn = sqlite3.connect(DB_NAME)
                conn.execute("""
                    INSERT INTO citizens (fio, phone, email, passport, diploma, workbook, skills, gdpr, current_status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Обучение')
                """, (c_fio.strip(), c_phone.strip(), c_email.strip(), c_pass.strip(), c_diploma.strip(), c_work.strip(), c_skills.strip(), 1 if c_gdpr else 0))
                conn.commit()
                conn.close()
                st.toast("Анкета успешно сохранена в реляционной СУБД SQLite!")
                st.rerun()

    # Блок теста компетенций (ФИКС ИНДЕНТАЦИИ КНОПКИ)
    with st.form("test_form"):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>🤖 Тест компетенций на производстве</h4>", unsafe_allow_html=True)
        st.markdown("**КЕЙС:** Критическая аварийная ситуация: Датчик стойки управления Syntec выдал перегрев шпинделя станка ЧПУ за 20 млн рублей. Ваши действия?")
        ans = st.radio("Выберите правильный алгоритм действий:", [
            "Игнорировать и закончить деталь",
            "Нажать аварийную кнопку STOP, перекрыть СОЖ и вызвать мастера",
            "Снизить обороты шпинделя вручную на 20%"
        ], index=None)
        
        if st.form_submit_button("Отправить ответы экзамена", type="primary"):
            if ans == "Нажать аварийную кнопку STOP, перекрыть СОЖ и вызвать мастера":
