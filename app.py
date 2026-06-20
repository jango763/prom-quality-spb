import streamlit as st
import pandas as pd
import random
import sqlite3
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТРОГИЕ КОРПОРАТИВНЫЕ СТИЛИ
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
    
    # Схема курсов ДПО
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            factory_inn TEXT,
            course_title TEXT,
            equipment_model TEXT,
            safety_instructions TEXT,
            tag_cnc INTEGER,
            tag_robot INTEGER,
            tag_hydro INTEGER,
            secret_question TEXT,
            secret_answer TEXT
        )
    """)
    
    # Схема соискателей / граждан РФ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            phone TEXT,
            district TEXT,
            current_education TEXT,
            current_status TEXT,
            assigned_course_id INTEGER
        )
    """)
    
    # Наполнение эталонными b2b-данными ОПК Санкт-Петербурга
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone() == 0:
        # Принудительная очистка старых поврежденных таблиц
        cursor.execute("DROP TABLE IF EXISTS factories") 
        
        cursor.execute("""
            INSERT INTO courses (factory_inn, course_title, equipment_model, safety_instructions, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
            VALUES ('7805041230', 'Комплексная наладка и эксплуатация тяжелых токарных комплексов', 'ЧПУ серии ИТ-42 (стойка Syntec)', 
            'ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ ЗАВОДА:\n1. Перед стартом проверить уровень масла в баке гидропривода.\n2. Критическое давление пресса и зажимных гидроцилиндров — выше 5 МПа.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание аварии на станке стоимостью 20 млн+.', 1, 0, 1,
            'Какое давление в гидросистеме является критическим для пресса?', 'Выше 5 МПа')
        """)
        
        cursor.executemany("""
            INSERT INTO citizens (fio, phone, district, current_education, current_status, assigned_course_id) VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("Никифоров Артур Владимирович (Выпускник СПбПУ)", "+7(921)555-44-33", "Кировский район", "Высшее техническое", "Железный специалист", 1),
            ("Смирнов Кирилл Михайлович (Соискатель)", "+7(911)888-77-66", "Калининский район", "Среднее профессиональное", "Направлен на практику", 1),
            ("Иванов Игорь Игоревич (Ученик)", "+7(900)111-22-33", "Приморский район", "Неполное высшее", "Обучение", 1)
        ])
    conn.commit()
    conn.close()

init_db()

# Данные промышленных гигантов для визуального мэтчинга
factories_data = pd.DataFrame([
    {"name": "АО «Кировский завод»", "inn": "7805041230", "district": "Кировский район"},
    {"name": "ПАО «Силовые машины» (ЛМЗ)", "inn": "7804014560", "district": "Калининский район"},
    {"name": "ОАО «ОДК-Климов»", "inn": "7814039910", "district": "Приморский район"}
])

# ==============================================================================
# 3. СЛОЙ ЖЕЛЕЗНОЙ БИЗНЕС-ЛОГИКИ (Контроллеры)
# ==============================================================================
def add_dpo_course(factory_inn, title, equipment, text, cnc, robot, hydro, q, a):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (factory_inn, course_title, equipment_model, safety_instructions, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (factory_inn, title, equipment, text, cnc, robot, hydro, q, a))
    conn.commit()
    conn.close()

def submit_custom_exam_results(citizen_id, course_id, user_answer_text, correct_answer_text):
    cleaned_user = str(user_answer_text).strip().lower()
    cleaned_correct = str(correct_answer_text).strip().lower()
    is_ok = (cleaned_user == cleaned_correct)
    new_status = "Тест сдан. Направлен на практику" if is_ok else "Обучение"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = ?, assigned_course_id = ? WHERE id = ?", (new_status, course_id, citizen_id))
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
    """ Безопасная кэшируемая выгрузка в один клик без сырых строк запроса """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT fio as 'ФИО соискателя', phone as 'Телефон', district as 'Район проживания', 
               current_status as 'Текущий статус готовности'
        FROM citizens WHERE current_status = 'Железный специалист'
    """, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Реестр_HR_ОПК')
    return output.getvalue()

# ==============================================================================
# 4. СЛОЙ ПРЕДСТАВЛЕНИЯ (views.py — Три автономных кабинета)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков АПП")
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        ["🏢 Личный кабинет Производственника", "🎓 Портал Гражданина РФ", "🛠️ Наш кабинет АПП (Управление экосистемой)"]
    )
    st.write("---")
    st.caption("Официальный комплекс Ассоциации промышленных предприятий СПб")

# Сбор KPI без строковых багов Pandas
conn = sqlite3.connect(DB_NAME)
total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
total_citizens = conn.execute("SELECT COUNT(*) FROM citizens").fetchone()[0]
ready_specialists = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()[0]
conn.close()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Развернутых b2b-программ", value=f"{int(total_courses)} моделей")
kpi2.metric(label="Граждан проходят квалификацию", value=f"{int(total_citizens)} соискателей")
kpi3.metric(label="Верифицировано «Железных специалистов»", value=f"{int(ready_specialists)} мастеров")
st.write("---")

# --- КАБИНЕТ 1: ЗАВОД ---
if user_role == "🏢 Личный кабинет Производственника":
    st.header("🏢 Личный кабинет Завода-Производителя оборудования")
    st.markdown('<div class="italy-box"><b>💡 Логика Итальянских Мастеров:</b> Выкладывайте развернутые обучающие материалы по вашим передовым станкам. Граждане РФ обучатся работе именно на ваших технологиях, формируя спрос на закупку вашего оборудования.</div>', unsafe_allow_html=True)
    
    tab_upload, tab_hr_registry = st.tabs(["📥 Сконструировать кадровый заказ и ДПО курс", "📋 Мониторинг статуса готовности рабочих"])
    
    with tab_upload:
        with st.form("dpo_upload_form"):
            f_name = st.selectbox("Выберите ваше зарегистрированное предприятие:", list(factories_data["name"]))
            f_row = factories_data[factories_data["name"] == f_name].iloc[0]
            st.caption(f"⚙️ Верифицированный ИНН: **{f_row['inn']}** | Локация: **{f_row['district']}**")
            
            c_title = st.text_input("Название программы опережающего ДПО:")
            e_model = st.text_input("Модель дорогостоящего промышленного станка:", value="Станок ЧПУ 20млн+")
            
