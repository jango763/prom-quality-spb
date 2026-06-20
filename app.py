import streamlit as st
import pandas as pd
import sqlite3
import io

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТИЛИ (Прошлый b2b-дизайн)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Система Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #334155; }
        div[data-testid="stMetricValue"] { font-size: 36px; font-weight: 800; color: #10B981; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px; border-radius: 12px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; }
        .hero-title { font-size: 32px; font-weight: 800; }
        .hero-subtitle { font-size: 15px; color: #94A3B8; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: white; }
        .status-ready { background-color: #10B981; }
        .status-process { background-color: #3B82F6; }
        .status-warning { background-color: #F59E0B; }
        .status-danger { background-color: #EF4444; }
        .matching-box { padding: 15px; border-radius: 8px; background-color: #ECFDF5; border-left: 5px solid #10B981; color: #065F46; font-weight: 600; margin-bottom: 15px; }
        .tag-pill { display: inline-block; background-color: #DBEAFE; color: #1E4ED8; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-right: 5px; }
        
        .metric-right-container {
            padding-left: 40px;
            border-left: 4px solid #E2E8F0;
            margin-top: 5px;
        }
        .metric-ready-title {
            font-size: 16px;
            font-weight: 700;
            color: #475569;
            margin-bottom: 8px;
        }
        .metric-ready-value {
            font-size: 48px;
            font-weight: 900;
            color: #10B981;
            line-height: 1;
        }
    </style>
""", unsafe_allow_html=True)

DB_NAME = "production_control_final_v5.db"

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ И СТРУКТУРА БАЗЫ ДАННЫХ SQLite
# ==============================================================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factory_name TEXT,
            course_title TEXT,
            equipment_model TEXT,
            safety_instructions TEXT,
            district TEXT,
            tag_cnc INTEGER,
            tag_robot INTEGER,
            tag_hydro INTEGER,
            secret_question TEXT,
            secret_answer TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            phone TEXT,
            district TEXT,
            current_education TEXT,
            current_status TEXT,
            course_id INTEGER
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
            VALUES ('АО «Кировский завод»', 'Цифровые стандарты безопасности «ПромКачество»', 'ЧПУ серии ИТ-42 (стойка Syntec)', 
            'ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ ЗАВОДА:\n1. Перед стартом проверить уровень масла в баке гидропривода.\n2. Критическое давление пресса и зажимных гидроцилиндров — выше 5 МПа.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание аварии на станке стоимостью 20 млн+.', 'Кировский район', 1, 0, 1,
            'Какое давление в гидросистеме является критическим для пресса?', 'Выше 5 МПа')
        """)
        
        cursor.executemany("""
            INSERT INTO citizens (fio, phone, district, current_education, current_status, course_id) VALUES (?, ?, ?, ?, ?, 1)
        """, [
            ("Никифоров Артур Владимирович", "+7(921)555-44-33", "Кировский район", "Высшее техническое", "Железный специалист"),
            ("Смирнов Кирилл Михайлович", "+7(911)888-77-66", "Калининский район", "Среднее профессиональное", "Направлен на практику"),
            ("Иванов Игорь Игоревич", "+7(900)111-22-33", "Приморский район", "Неполное высшее", "Обучение")
        ])
    conn.commit()
    conn.close()

init_db()

factories_static = {
    "АО «Кировский завод»": {"inn": "7805041230", "district": "Кировский район"},
    "ПАО «Силовые машины» (ЛМЗ)": {"inn": "7804014560", "district": "Калининский район"},
    "ОАО «ОДК-Климов»": {"inn": "7814039910", "district": "Приморский район"}
}

# ==============================================================================
# 3. ЕДИНАЯ НАВИГАЦИЯ САЙДБАРА
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков АПП")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        ["🏢 Личный кабинет Производственника", "🎓 Портал Гражданина РФ", "🛠️ Наш кабинет АПП (Управление экосистемой)"]
    )
    st.write("---")
    st.caption("Официальная платформа АПП Санкт-Петербурга")

st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
    </div>
""", unsafe_allow_html=True)

# Чтение актуальных данных через Pandas (Просто и без багов с KeyError)
conn = sqlite3.connect(DB_NAME)
courses_df = pd.read_sql_query("SELECT * FROM courses", conn)
citizens_df = pd.read_sql_query("SELECT * FROM citizens", conn)
conn.close()

# KPI-Метрики в шапке
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернутых b2b-курсов", value=f"{len(courses_df)} моделей")
kpi2.metric(label="Граждан в системе ДПО", value=f"{len(citizens_df)} соискателей")
ready_cnt = len(citizens_df[citizens_df['current_status'] == 'Железный специалист'])
kpi3.metric(label="Верифицировано «Железных специалистов»", value=f"{ready_cnt} мастеров")
st.write("---")

# ==============================================================================
# КАБИНЕТ 1: 🏢 ЛИЧНЫЙ КАБИНЕТ ПРОИЗВОДСТВЕННИКА (B2B)
# ==============================================================================
if user_role == "🏢 Личный кабинет Производственника":
    st.header("🏢 Личный кабинет Завода-Производителя оборудования")
    st.markdown('<div class="matching-box"><b>💡 Логика Итальянских Мастеров:</b> Выкладывайте развернутые обучающие материалы по вашим передовым станкам. Граждане РФ обучатся работе именно на ваших технологиях, формируя спрос на закупку вашего оборудования.</div>', unsafe_allow_html=True)
    
    tab_upload, tab_hr_registry = st.tabs(["📥 Сконструировать кадровый заказ и ДПО курс", "📋 Реестр проверенных специалистов HR"])
    
    with tab_upload:
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Ваш остаток на счете подбора", value="25,000.00 ₽")
        with col_m2:
            st.metric(label="Ваш текущий тариф", value="БЕЗЛИМИТНЫЙ ГОДОВОЙ НАЙМ")
        with col_m3:
            # Сдвиг счетчика готовых кандидатов правее
            st.markdown(f"""
                <div class="metric-right-container">
                    <div class="metric-ready-title">Готовых кандидатов в базе</div>
                    <div class="metric-ready-value">{ready_cnt}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        
        with st.form("dpo_upload_form", clear_on_submit=True):
            f_name = st.selectbox("Выберите ваше зарегистрированное предприятие:", list(factories_static.keys()))
            st.caption(f"⚙️ Верифицированный ИНН: **{factories_static[f_name]['inn']}** | Локация: **{factories_static[f_name]['district']}**")
            
            c_title = st.text_input("Название программы опережающего ДПО:")
            e_model = st.text_input("Модель дорогостоящего промышленного станка:", value="Станок ЧПУ 20млн+")
            
            st.markdown("**🛠️ Выберите технологические направления оборудования (Теги найма):**")
            c_cnc = st.checkbox("ЧПУ-комплексы и обрабатывающие центры", value=True)
            c_robot = st.checkbox("Робототехника / Автоматизация цеха")
            c_hydro = st.checkbox("Промышленная гидравлика и тяжелые прессы")
            
            s_instructions = st.text_area("Развернутый текст регламента безопасности и эксплуатации станка:")
            sec_q = st.text_input("Сконструируйте кастомный секретный вопрос по ТБ:", value="Какое давление в гидросистеме является критическим для пресса?")
            sec_a = st.text_input("Внесите эталонный правильный ответ:", value="Выше 5 МПа")
            
            if st.form_submit_button("Опубликовать комплексные требования завода", use_container_width=True):
                if c_title.strip() and s_instructions.strip():
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("""
                        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
