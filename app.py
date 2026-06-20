import streamlit as st
import pandas as pd
import random
import sqlite3
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТИЛИ
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Система Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #334155; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #10B981; }
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
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (SQLite в режиме WAL с авто-очисткой структуры)
# ==============================================================================
DB_NAME = "production_control.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col] = row[idx]
    return d

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # ПРИНУДИТЕЛЬНЫЙ СБРОС СТАРЫХ НЕСТАБИЛЬНЫХ ТАБЛИЦ ДЛЯ УСТРАНЕНИЯ OPERATIONALERROR
    cursor.execute("DROP TABLE IF EXISTS courses;")
    cursor.execute("DROP TABLE IF EXISTS citizens;")
    
    # Создание чистой актуальной схемы курсов ДПО
    cursor.execute("""
        CREATE TABLE courses (
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
    
    # Создание чистой актуальной схемы соискателей
    cursor.execute("""
        CREATE TABLE citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            phone TEXT,
            district TEXT,
            current_education TEXT,
            current_status TEXT,
            course_id INTEGER
        )
    """)
    
    # Наполнение верифицированными b2b-данными под Демо-день
    cursor.execute("""
        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
        VALUES ('АО «Кировский завод»', 'Цифровые стандарты безопасности «ПромКачество»', 'ЧПУ серии ИТ-42 (стойка Syntec)', 
        'ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ ЗАВОДА:\n1. Перед стартом проверить уровень масла в баке гидропривода.\n2. Критическое давление пресса и зажимных гидроцилиндров — выше 5 МПа.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание аварии на станке стоимостью 20 млн+.', 'Кировский район', 1, 0, 1,
        'Какое давление в гидросистеме является критическим для пресса?', 'Выше 5 МПа')
    """)
    
    cursor.executemany("""
        INSERT INTO citizens (fio, phone, district, current_education, current_status, course_id) VALUES (?, ?, ?, ?, ?, 1)
    """, [
        ("Никифоров Артур Владимирович", "+7(921)555-44-33", "Кировский район", "Высшее техническое", "Железный專员", 1),
        ("Смирнов Кирилл Михайлович", "+7(911)888-77-66", "Калининский район", "Среднее профессиональное", "Направлен на практику", 1),
        ("Иванов Игорь Игоревич", "+7(900)111-22-33", "Приморский район", "Неполное высшее", "Обучение", 1)
    ])
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = 1")
    conn.commit()
    conn.close()

init_db()

factories_static = {
    "АО «Кировский завод»": {"inn": "7805041230", "district": "Кировский район"},
    "ПАО «Силовые машины» (ЛМЗ)": {"inn": "7804014560", "district": "Калининский район"},
    "ОАО «ОДК-Климов»": {"inn": "7814039910", "district": "Приморский район"}
}

def fetch_all_from_db(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(query, params)
    res = cursor.fetchall()
    conn.close()
    return res

# ==============================================================================
# 3. НАВИГАЦИЯ (САЙДБАР)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков АПП")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        ["🏢 Личный кабинет Производственника", "🎓 Портал Гражданина РФ", "🛠️ Наш кабинет АПП (Управление экосистемой)"]
    )
    st.write("---")
    st.caption("Ассоциация промышленных предприятий СПб")

st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
    </div>
""", unsafe_allow_html=True)

courses_list = fetch_all_from_db("SELECT * FROM courses")
citizens_list = fetch_all_from_db("SELECT * FROM citizens")

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернутых b2b-курсов", value=f"{len(courses_list)} моделей")
kpi2.metric(label="Граждан в системе ДПО", value=f"{len(citizens_list)} соискателей")
ready_cnt = sum(1 for c in citizens_list if c['current_status'] == 'Железный специалист')
kpi3.metric(label="Верифицировано «Железных специалистов»", value=f"{ready_cnt} мастеров")
st.write("---")

# ==============================================================================
# КАБИНЕТ 1: 🏢 ЛИЧНЫЙ КАБИНЕТ ПРОИЗВОДСТВЕННИКА (B2B)
# ==============================================================================
if user_role == "🏢 Личный кабинет Производственника":
    st.header("🏢 Личный кабинет Завода-Производителя оборудования")
    st.markdown('<div class="italy-box"><b>💡 Логика Итальянских Мастеров:</b> Выкладывайте развернутые обучающие материалы по вашим передовым станкам. Граждане РФ обучатся работе именно на ваших технологиях, формируя спрос на закупку вашего оборудования.</div>', unsafe_allow_html=True)
    
    tab_upload, tab_hr_registry = st.tabs(["📥 Сконструировать кадровый заказ и ДПО курс", "📋 Реестр проверенных специалистов HR"])
    
    with tab_upload:
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
                    """, (f_name, c_title.strip(), e_model.strip(), s_instructions.strip(), factories_static[f_name]['district'], 1 if c_cnc else 0, 1 if c_robot else 0, 1 if c_hydro else 0, sec_q.strip(), sec_a.strip()))
                    conn.commit()
                    conn.close()
                    st.success("Кадровый заказ успешно опубликован в базе данных SQLite!")
                    st.rerun()
                else:
                    st.error("Заполните форму!")
                    
    with tab_hr_registry:
        st.subheader("Реестр соискателей в системе контроля квалификации:")
        for citizen in citizens_list:
            with st.container(border=True):
                st.markdown(f"### 👤 Специалист: {citizen['fio']}")
