import streamlit as st
import pandas as pd
import sqlite3
import io

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТРОГИЙ B2B-ДИЗАЙН
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Контур Квалификации", layout="wide", page_icon="🏭")

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

DB_NAME = "production_control.db"

# ==============================================================================
# 2. СЛОЙ ДАННЫХ (SQLite Схема — Связи по ИНН завода и ID соискателя)
# ==============================================================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Принудительный сброс старых конфликтных таблиц
    cursor.execute("DROP TABLE IF EXISTS courses;")
    cursor.execute("DROP TABLE IF EXISTS citizens;")
    cursor.execute("DROP TABLE IF EXISTS test_attempts;")
    
    # Схема курсов ДПО
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
    
    # Схема соискателей
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
    
    # Таблица попыток тестов
    cursor.execute("""
        CREATE TABLE test_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citizen_id INTEGER,
            course_id INTEGER,
            score INTEGER,
            is_passed TEXT
        )
    """)
    
    # Первичное наполнение базы под Демо-день
    cursor.execute("""
        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
        VALUES ('АО «Кировский завод»', 'Цифровые стандарты безопасности «ПромКачество»', 'ЧПУ серии ИТ-42 (стойка Syntec)', 
        'ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ ЗАВОДА:\n1. Перед стартом проверить уровень масла в баке гидропривода.\n2. Критическое давление пресса и зажимных гидроцилиндров — выше 5 МПа.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание аварии на станке стоимостью 20 млн+.', 'Кировский район', 1, 0, 1,
        'Какое давление в гидросистеме является критическим для пресса?', 'Выше 5 МПа')
    """)
    
    cursor.execute("""
        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
        VALUES ('ПАО «Силовые машины» (ЛМЗ)', 'Допуск к измерительному оборудованию хаба', 'ЛМЗ-Гидро-2026', 
        'ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ ЗАВОДА:\n1. Убедиться в отсутствии посторонних предметов в камере рабочего колеса.\n2. Использовать динамометрический инструмент.\n3. Запрещено проводить работы без заземления станины.', 'Калининский район', 1, 1, 0,
        'Какое действие необходимо совершить перед запуском гидротурбины?', 'Проверить заземление станины')
    """)
    
    # Исправленные 6 знаков вопроса под 6 элементов кортежей
    cursor.executemany("""
        INSERT INTO citizens (fio, phone, district, current_education, current_status, course_id) VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("Никифоров Артур Владимирович (Выпускник СПбПУ)", "+7(921)555-44-33", "Кировский район", "Высшее техническое", "Железный专员", 1),
        ("Смирнов Кирилл Михайлович (Соискатель)", "+7(911)888-77-66", "Калининский район", "Среднее профессиональное", "Направлен на практику", 1),
        ("Иванов Игорь Игоревич (Ученик)", "+7(900)111-22-33", "Приморский район", "Неполное высшее", "Обучение", 1)
    ])
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = 1")
    cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (1, 1, 3, 'True')")
    cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (2, 2, 3, 'True')")
    
    conn.commit()
    conn.close()

init_db()

factories_static = {
    "АО «Кировский завод»": {"inn": "7805041230", "district": "Кировский район"},
    "ПАО «Силовые машины» (ЛМЗ)": {"inn": "7804014560", "district": "Калининский район"},
    "ОАО «ОДК-Климов»": {"inn": "7814039910", "district": "Приморский район"}
}

# ==============================================================================
# 3. СЛОЙ ЖЕЛЕЗНОЙ БИЗНЕС-ЛОГИКИ (Контроллеры)
# ==============================================================================
def add_dpo_course(factory, title, equipment, text, cnc, robot, hydro, q, a):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, district, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (factory, title, equipment, text, factories_static[factory]['district'], cnc, robot, hydro, q, a))
    conn.commit()
    conn.close()

def submit_custom_exam_results(citizen_id, course_id, user_answer_text, correct_answer_text):
    cleaned_user = str(user_answer_text).strip().lower()
    cleaned_correct = str(correct_answer_text).strip().lower()
    is_ok = (cleaned_user == cleaned_correct)
    new_status = "Тест сдан. Направлен на практику" if is_ok else "Обучение"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = ?, course_id = ? WHERE id = ?", (new_status, course_id, citizen_id))
    cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (?, ?, ?, ?)", 
                   (citizen_id, course_id, 3 if is_ok else 0, "True" if is_ok else "False"))
    conn.commit()
    conn.close()
    return is_ok

def enroll_to_practice(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'Направлен на практику' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

def approve_practice_specialist(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

@st.cache_data(ttl=60)
def generate_hr_excel_report():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT c.fio as 'ФИО проверенного мастера', c.phone as 'Телефон', c.current_education as 'Образование',
               crs.equipment_model as 'Аттестованный станок', crs.factory_name as 'Завод-заказчик'
        FROM citizens c
        JOIN courses crs ON c.course_id = crs.id
        WHERE c.current_status = 'Железный специалист'
    """, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# ==============================================================================
# 4. НАВИГАЦИЯ И ИНТЕРФЕЙС (views.py — Три автономных кабинета)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков АПП")
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        ["🏢 Личный кабинет Производственника", "🎓 Портал Гражданина РФ", "🛠️ Наш кабинет АПП (Управление экосистемой)"]
    )
    st.write("---")
    st.caption("Ассоциация промышленных предприятий СПб")

# Живые b2b-метрики из базы данных
conn = sqlite3.connect(DB_NAME)
total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
total_citizens = conn.execute("SELECT COUNT(*) FROM citizens").fetchone()[0]
ready_specialists = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()[0]
conn.close()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернутых b2b-курсов", value=f"{total_courses} моделей")
kpi2.metric(label="Граждан в системе ДПО", value=f"{total_citizens} соискателей")
