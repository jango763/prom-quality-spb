import streamlit as st
import pandas as pd
import sqlite3
import io
import html

# ==============================================================================
# 1. СТРОГАЯ КОРПОРАТИВНАЯ СТИЛИЗАЦИЯ (Индустриальная айдентика АПП СПб)
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

# ==============================================================================
# 2. СЛОЙ ДАННЫХ (SQLite Схема — Связи по ИНН завода и ID соискателя)
# ==============================================================================
DB_NAME = "app_qualification_control.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # АКТИВАЦИЯ РЕЖИМА WAL ДЛЯ МНОГОПОТОЧНОЙ СТАБИЛЬНОСТИ
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Таблица заводов (Уникальный ИНН является ключом)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS factories (
            inn TEXT PRIMARY KEY,
            factory_name TEXT,
            district TEXT
        )
    """)
    
    # Таблица курсов / требований (Связана с заводами по factory_inn)
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
            secret_answer TEXT,
            FOREIGN KEY(factory_inn) REFERENCES factories(inn)
        )
    """)
    
    # Таблица соискателей / граждан РФ (district для гео-мэтчинга)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT,
            phone TEXT,
            district TEXT,
            current_education TEXT,
            current_status TEXT,
            assigned_course_id INTEGER,
            FOREIGN KEY(assigned_course_id) REFERENCES courses(id)
        )
    """)
    
    # Наполнение эталонными b2b-данными ОПК Санкт-Петербурга для Демо-дня
    cursor.execute("SELECT COUNT(*) FROM factories")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO factories VALUES ('7805041230', 'АО «Кировский завод»', 'Кировский район')")
        cursor.execute("INSERT INTO factories VALUES ('7804014560', 'ПАО «Силовые машины» (ЛМЗ)', 'Калининский район')")
        
        cursor.execute("""
            INSERT INTO courses (factory_inn, course_title, equipment_model, safety_instructions, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
            VALUES ('7805041230', 'Комплексная наладка и эксплуатация тяжелых токарных комплексов', 'ЧПУ серии ИТ-42 (стойка Syntec)', 
            'ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ ЗАВОДА:\n1. Перед стартом проверить уровень масла в баке гидропривода.\n2. Критическое давление пресса и зажимных гидроцилиндров — выше 5 МПа.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание аварии на станке стоимостью 20 млн+.', 1, 0, 1,
            'Какое давление в гидросистеме является критическим для пресса?', 'Выше 5 МПа')
        """)
        
        cursor.executemany("""
            INSERT INTO citizens (fio, phone, district, current_education, current_status, assigned_course_id) VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("Никифоров Артур Владимирович (Выпускник СПбПУ)", "+7(921)555-44-33", "Кировский район", "Высшее техническое", "Железный專员", 1), # Исправим статус ниже
            ("Смирнов Кирилл Михайлович (Соискатель)", "+7(911)888-77-66", "Калининский район", "Среднее профессиональное", "Направлен на практику", 1),
            ("Иванов Игорь Игоревич (Ученик)", "+7(900)111-22-33", "Приморский район", "Неполное высшее", "Обучение", 1)
        ])
        cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = 1")
        
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# 3. СЛОЙ ЖЕЛЕЗНОЙ БИЗНЕС-ЛОГИКИ (Жесткие функции-контроллеры)
# ==============================================================================
def add_dpo_course(factory_inn, title, equipment, text, cnc, robot, hydro, q, a):
    """ Регистрирует и выводит стандарты завода в единый каталог курсов """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (factory_inn, course_title, equipment_model, safety_instructions, tag_cnc, tag_robot, tag_hydro, secret_question, secret_answer) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (factory_inn, title, equipment, text, cnc, robot, hydro, q, a))
    conn.commit()
    conn.close()

def submit_custom_exam_results(citizen_id, course_id, user_answer_text, correct_answer_text):
    """ FIX #2: Очистка (.strip().lower()) и программная проверка ответа автоматикой """
    cleaned_user = str(user_answer_text).strip().lower()
    cleaned_correct = str(correct_answer_text).strip().lower()
    
    # Нулевая толерантность: совпадение 100% или жесткий отсев
    is_ok = (cleaned_user == cleaned_correct)
    new_status = "Тест сдан. Направлен на практику" if is_ok else "Обучение"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = ?, assigned_course_id = ? WHERE id = ?", (new_status, course_id, citizen_id))
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
    """ FIX #3: Финальное ручное b2b-подтверждение практики наставником цеха """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

@st.cache_data(ttl=60)
def generate_hr_excel_report():
    """ FIX #4: Безопасный экспорт реестра готовых кадров в Excel через io.BytesIO() """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT c.fio as 'ФИО проверенного мастера', c.phone as 'Телефон', c.current_education as 'Образование',
               crs.equipment_model as 'Аттестованный станок', f.factory_name as 'Завод-заказчик', f.inn as 'ИНН завода'
        FROM citizens c
        JOIN courses crs ON c.assigned_course_id = crs.id
        JOIN factories f ON crs.factory_inn = f.inn
        WHERE c.current_status = 'ЖелезныйBox' OR c.current_status = 'Железный специалист'
    """, conn)
    conn.close()
    
    output = io.BytesIO() # Контекстный менеджер io.BytesIO защищает ОЗУ сервера от утечек памяти
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Железные_Специалисты_HR')
    return output.getvalue()

# ==============================================================================
# 4. СЛОЙ ИНТЕРФЕЙСА (views.py — Три автономных кабинета в st.tabs)
# ==============================================================================
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Цифровая b2b2c-экосистема контроля квалификации «ПромКачество»</div>
        <div class="hero-subtitle">Комплексный ИТ-конструктор допусков к высокотехнологичному оборудованию ОПК Санкт-Петербурга</div>
    </div>
""", unsafe_allow_html=True)

# Сбор глобальных KPI из БД для демонстрации инвесторам
conn = sqlite3.connect(DB_NAME)
kpi_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
kpi_citizens = conn.execute("SELECT COUNT(*) FROM citizens").fetchone()[0]
kpi_ready = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()[0]
conn.close()

m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric(label="Индустриальных b2b-курсов в каталоге", value=f"{int(kpi_courses)} моделей станков")
m_col2.metric(label="Граждан РФ проходят аттестацию", value=f"{int(kpi_citizens)} соискателей")
m_col3.metric(label="Сертифицировано «Железных специалистов»", value=f"{int(kpi_ready)} мастеров")
st.write("---")

