import streamlit as st
import pandas as pd
import random
import sqlite3
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТРОГИЕ КОРПОРАТИВНЫЕ СТИЛИ (Дизайн Сбера/Яндекса)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Контур Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #334155; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #10B981; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px; border-radius: 12px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; }
        .hero-title { font-size: 32px; font-weight: 800; }
        .hero-subtitle { font-size: 15px; color: #94A3B8; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: white; }
        .italy-box { padding: 20px; background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; color: #166534; margin-bottom: 20px; }
        .simulator-box { padding: 25px; background-color: #1E293B; color: #F8FAFC; border-radius: 12px; font-family: 'Courier New', Courier, monospace; border-left: 6px solid #38BDF8; margin-top: 15px; }
        .passport-tag { display: inline-block; background-color: #E2E8F0; color: #334155; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; margin-right: 5px; margin-bottom: 5px; }
        .status-ready { background-color: #10B981; }
        .status-process { background-color: #3B82F6; }
        .status-warning { background-color: #F59E0B; }
        .status-danger { background-color: #EF4444; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (SQLite — Строгая схема из Финальной Директивы)
# ==============================================================================
DB_NAME = "production_control.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица 1: Курсы заводов (courses)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, factory_name TEXT, course_title TEXT, 
            equipment_model TEXT, safety_instructions TEXT, lat REAL, lon REAL, district TEXT
        )
    """)
    
    # Таблица 2: Пользователи / Граждане РФ (citizens)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fio TEXT, phone TEXT, district TEXT, current_status TEXT
        )
    """)
    
    # Таблица 3: Попытки сдачи тестов (test_attempts)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, citizen_id INTEGER, course_id INTEGER, score INTEGER, is_passed TEXT
        )
    """)
    
    # Наполнение эталонными b2b-данными ОПК Санкт-Петербурга для Демо-дня
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone() == 0:
        cursor.executemany("""
            INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, lat, lon, district) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            ("АО «Кировский завод»", "Цифровые стандарты безопасности «ПромКачество»", "ЧПУ серии ИТ-42 (стойка Syntec)", "ПРАВИЛА БЕЗОПАСНОСТИ СТАНКА:\n1. Перед запуском цикла ЧПУ обязательно проверить уровень масла в баке гидропривода (норма 4.5-5.0 бар).\n2. При аварийном росте давления немедленно активировать ручной сброс через клапан А-3.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание поломки резца за 20 млн рублей.", 59.8789, 30.2644, "Кировский район"),
            ("ПАО «Силовые машины» (ЛМЗ)", "Допуск к оборудованию шеринг-хаба", "ЛМЗ-Гидро-2026", "ПРАВИЛА БЕЗОПАСНОСТИ СТАНКА:\n1. Перед запуском цикла ЧПУ обязательно проверить уровень масла в баке гидропривода (норма 4.5-5.0 бар).\n2. При аварийном росте давления немедленно активировать ручной сброс через клапан А-3.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание поломки резца за 20 млн рублей.", 59.9572, 30.3842, "Калининский район"),
            ("ОАО «ОДК-Климов»", "Сертификация по оборонным стандартам", "Испытательный стенд ВК-2500", "ПРАВИЛА БЕЗОПАСНОСТИ СТАНКА:\n1. Перед запуском цикла ЧПУ обязательно проверить уровень масла в баке гидропривода (норма 4.5-5.0 бар).\n2. При аварийном росте давления немедленно активировать ручной сброс через клапан А-3.\n3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание поломки резца за 20 млн рублей.", 60.0247, 30.3015, "Приморский район")
        ])
        
        cursor.executemany("""
            INSERT INTO citizens (fio, phone, district, current_status) VALUES (?, ?, ?, ?)
        """, [
            ("Александров К.М. (Военмех)", "+7(921)345-67-89", "Кировский район", "Железный专员"), # Будет обновлен до 'Железный специалист' контроллером
            ("Дмитриев А.В. (СПбПУ)", "+7(911)987-65-43", "Калининский район", "На практике"),
            ("Иванов И.И. (Колледж ОПК)", "+7(900)111-22-33", "Приморский район", "Обучение")
        ])
        # Принудительно выставляем корректный статус
        cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = 1")
        cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (1, 1, 3, 'True')")
        cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (2, 2, 3, 'True')")
        
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# 3. СЛОЙ ЖЕЛЕЗНОЙ БИЗНЕС-ЛОГИКИ (4 Функции-Контроллера + Безопасный Excel)
# ==============================================================================
def add_dpo_course(factory, title, equipment, text):
    """ Сохраняет развернутый регламент завода в общую базу данных """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions, lat, lon, district) 
        VALUES (?, ?, ?, ?, 59.9343, 30.3351, 'Центральный район')
    """, (factory, title, equipment, text))
    conn.commit()
    conn.close()

def submit_test_results(citizen_id, course_id, score):
    """ FIX #2: Программная проверка теста ТБ. Если 3/3 — сдал, иначе — блокировка """
    is_passed = "True" if score == 3 else "False"
    new_status = "Тест сдан. Ждет практику" if score == 3 else "Обучение"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (?, ?, ?, ?)",
                   (citizen_id, course_id, score, is_passed))
    cursor.execute("UPDATE citizens SET current_status = ? WHERE id = ?", (new_status, citizen_id))
    conn.commit()
    conn.close()
    return score == 3

def enroll_to_practice(citizen_id):
    """ Переводит соискателя на этап практики в цеху """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'На практике' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

def approve_practice(citizen_id):
    """ FIX #3: Мастер цеха подтверждает успешное прохождение практики """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'Железный專员' WHERE id = ?", (citizen_id,))
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

@st.cache_data(ttl=60)
def generate_excel_report():
    """ FIX #4: Безопасный генератор отчетов с TTL=60 сек. Без произвольных SQL инъекций. """
    conn = sqlite3.connect(DB_NAME)
    # Запрос жестко зашит: выгружаются ТОЛЬКО проверенные мастера
    df = pd.read_sql_query("""
        SELECT c.fio as 'ФИО Мастера', c.phone as 'Телефон связи', c.district as 'Район проживания', 
               crs.factory_name as 'Завод-аттестатор', crs.equipment_model as 'Допуск к оборудованию'
        FROM citizens c
        JOIN test_attempts ta ON c.id = ta.citizen_id
        JOIN courses crs ON ta.course_id = crs.id
        WHERE c.current_status = 'Железный специалист' AND ta.is_passed = 'True'
    """, conn)
    conn.close()
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Верифицированные_Кадры')
    return output.getvalue()

# ==============================================================================
# 4. СЛОЙ ПРЕДСТАВЛЕНИЯ (Экранные формы — views.py)
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Допусков")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        ["🏢 Личный кабинет Производственника", "🎓 Портал Гражданина РФ"]
    )
    st.write("---")
    st.caption("Официальный стек Ассоциации промышленных предприятий СПб")

# Живые b2b-метрики из базы данных
conn = sqlite3.connect(DB_NAME)
total_courses = pd.read_sql_query("SELECT COUNT(*) as cnt FROM courses", conn).loc[0, 'cnt']
total_citizens = pd.read_sql_query("SELECT COUNT(*) as cnt FROM citizens", conn).loc[0, 'cnt']
ready_specialists = pd.read_sql_query("SELECT COUNT(*) as cnt FROM citizens WHERE current_status='Железный специалист'", conn).loc[0, 'cnt']
