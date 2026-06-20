import streamlit as st
import pandas as pd
import random
import sqlite3
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТРОГИЙ B2B-ДИЗАЙН
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | ИТ-Конструктор", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #334155; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #10B981; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px; border-radius: 12px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; }
        .hero-title { font-size: 32px; font-weight: 800; }
        .hero-subtitle { font-size: 15px; color: #94A3B8; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: white; }
        .italy-box { padding: 20px; background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; color: #166534; margin-bottom: 20px; }
        .matching-box { padding: 15px; border-radius: 8px; background-color: #ECFDF5; border-left: 5px solid #10B981; color: #065F46; font-weight: 600; margin-bottom: 15px; }
        .status-ready { background-color: #10B981; }
        .status-process { background-color: #3B82F6; }
        .status-warning { background-color: #F59E0B; }
        .status-danger { background-color: #EF4444; }
        .tag-pill { display: inline-block; background-color: #DBEAFE; color: #1E4ED8; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-right: 5px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (SQLite в режиме WAL — Многопоточный b2b-контур)
# ==============================================================================
DB_NAME = "production_control.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Схема курсов ДПО (Добавлены теги направлений и поля секретного b2b-теста)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, factory_name TEXT, course_title TEXT, 
            equipment_model TEXT, safety_instructions TEXT, district TEXT,
            tag_cnc INTEGER, tag_robot INTEGER, tag_hydro INTEGER,
            secret_question TEXT, secret_answer TEXT, contract_years INTEGER, penalty_amount REAL
        )
    """)
    
    # Схема пользователей (citizens)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fio TEXT, phone TEXT, district TEXT, 
            current_status TEXT, is_contract_signed INTEGER
        )
    """)
    
    # Проверка дефолтных b2b-профилей для Демо-дня
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone() == 0:
        cursor.execute("""
            INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer, contract_years, penalty_amount) 
            VALUES (?, ?, ?, ?, ?, 1, 0, 1, ?, ?, ?, ?)
        """, (
            "АО «Кировский завод»", "Цифровые стандарты эксплуатации тяжелых прессов", "Прессовый комплекс КЗ-2026", 
            "ИНСТРУКЦИЯ: 1. Перед запуском проверить масло. 2. Критическое давление пресса — выше 5 МПа.", "Кировский район",
            "Какое давление в гидросистеме является критическим для пресса?", "Выше 5 МПа", 2, 150000.0
        ))
        
        cursor.executemany("""
            INSERT INTO citizens (fio, phone, district, current_status, is_contract_signed) VALUES (?, ?, ?, ?, ?)
        """, [
            ("Александров К.М. (Выпускник Военмех)", "+7(921)345-67-89", "Кировский район", "Железный специалист", 1),
            ("Дмитриев А.В. (Выпускник СПбПУ)", "+7(911)987-65-43", "Калининский район", "На практике", 1),
            ("Иванов И.И. (Колледж ОПК)", "+7(900)111-22-33", "Приморский район", "Обучение", 0)
        ])
        cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = 1")
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# 3. СЛОЙ ЖЕЛЕЗНОЙ БИЗНЕС-ЛОГИКИ (Контроллеры)
# ==============================================================================
def add_custom_b2b_course(factory, title, equipment, text, district, cnc, robot, hydro, q, a, years, penalty):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer, contract_years, penalty_amount) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (factory, title, equipment, text, district, cnc, robot, hydro, q, a, years, penalty))
    conn.commit()
    conn.close()

def sign_u_contract(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET is_contract_signed = 1 WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

def process_custom_exam(citizen_id, score_passed):
    new_status = "Тест сдан. Ждет практику" if score_passed else "Обучение"
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = ? WHERE id = ?", (new_status, citizen_id))
    conn.commit()
    conn.close()

def enroll_to_practice(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'На практике' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

def approve_practice(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

@st.cache_data(ttl=60)
def generate_excel_report():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT fio as 'ФИО соискателя', phone as 'Телефон', district as 'Район проживания', 
               current_status as 'Текущий статус готовности', 
               CASE WHEN is_contract_signed=1 THEN 'Подписан ЭЦП (Охрана кадров)' ELSE 'Не подписан' END as 'Юридический договор'
        FROM citizens
    """, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Сводная_Ведомость_АПП')
    return output.getvalue()

# ==============================================================================
# 4. СУПЕР-НАВИГАЦИЯ (3 ИЗОЛИРОВАННЫХ КАБИНЕТА)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Экосистема АПП")
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        ["🏢 Кабинет Завода-Производителя (B2B)", "🎓 Портал обучения Граждан РФ (B2C)", "🛠️ Наш кабинет АПП (Управление экосистемой)"]
    )
    st.write("---")
    st.caption("Комплекс Ассоциации промышленных предприятий СПб")

st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Гибкий ИТ-конструктор кадровых допусков и формирования b2b-рынков сбыта оборудования</div>
    </div>
""", unsafe_allow_html=True)

# Сбор KPI
conn = sqlite3.connect(DB_NAME)
total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
total_citizens = conn.execute("SELECT COUNT(*) FROM citizens").fetchone()[0]
ready_specialists = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()[0]
conn.close()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернутых b2b-программ в конструкторе", value=f"{int(total_courses)} моделей")
kpi2.metric(label="Граждан проходят квалификацию", value=f"{int(total_citizens)} соискателей")
kpi3.metric(label="Верифицировано «Железных специалистов»", value=f"{int(ready_specialists)} мастеров")
st.write("---")

# --- КАБИНЕТ 1: ЗАВОД (B2B ИТ-КОНСТРУКТОР ТРЕБОВАНИЙ) ---
if user_role == "🏢 Кабинет Завода-Производителя (B2B)":
    st.header("🏢 Инструмент вывода стандартов завода и защиты оборудования")
    st.markdown('<div class="italy-box"><b>💡 Логика Итальянских Мастеров:</b> Заложите свои уникальные технические требования и секретный проверочный вопрос по ТБ. Система автоматически перестроит экзаменационный фильтр для соискателей, гарантируя защиту ваших станков за 20 млн рублей.</div>', unsafe_allow_html=True)
    
    t_upload, t_registry = st.tabs(["📥 Сконструировать кадровый заказ и ДПО курс", "📋 Мониторинг статуса готовности рабочих"])
    
    with t_upload:
        with st.form("custom_b2b_builder_form"):
            st.subheader("1. Базовые параметры кадрового заказа:")
            f_name = st.text_input("Название предприятия:", value="АО «Кировский завод»")
            c_title = st.text_input("Название программы опережающего ДПО:")
            e_model = st.text_input("Модель дорогостоящего оборудования (Станка):", value="ЧПУ ИТ-42 (Syntec)")
            f_dist = st.selectbox("Район расположения производства:", ["Кировский район", "Калининский район", "Приморский район"])
            
            # ПУНКТ №1: Готовые чекбоксы технологических направлений
            st.markdown("**🛠️ Выберите технологические направления курса (активные теги):**")
            ch_cnc = st.checkbox("ЧПУ-комплексы и станочные центры")
