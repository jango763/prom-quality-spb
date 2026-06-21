import streamlit as st
import pandas as pd
import sqlite3

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И ОСОБЫЙ КИБЕРПАНК-СТИЛЬ ИЗ CODEPEN
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Система Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        /* Полное переопределение фона под тему CodePen */
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        
        /* Особый премиум Hero-баннер АПП */
        .hero-banner {
            background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important;
            padding: 35px; border-radius: 16px; color: #FFFFFF; margin-bottom: 25px;
            border-left: 8px solid #10B981; box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
        }
        .hero-title {
            font-size: 28px; font-weight: 800;
            background: linear-gradient(90deg, #10B981, #34D399);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hero-subtitle { font-size: 14px; color: #94A3B8; margin-top: 8px; line-height: 1.4; }

        /* Матовые B2B-контейнеры (Glassmorphism) */
        div[data-testid="stForm"], div[data-testid="stExpander"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 14px !important; padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important; backdrop-filter: blur(12px);
        }

        /* Объемные карточки KPI из CodePen */
        .glass-card {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px; padding: 20px; margin-bottom: 15px;
        }
        .card-title { font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ ОБЩЕЙ БАЗЫ ДАННЫХ SQLITE (WAL)
# ==============================================================================
DB_NAME = "production_control_enterprise_final_v1.db"

def init_db():
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
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# 3. ГЛАВНЫЙ ЭКРАН И ГЛОБАЛЬНЫЕ KPI ПЛАТФОРМЫ
# ==============================================================================
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ. Используйте боковое меню для перехода в личные кабинеты.</div>
    </div>
""", unsafe_allow_html=True)

# Считываем актуальные данные
conn = sqlite3.connect(DB_NAME)
citizens_df = pd.read_sql_query("SELECT * FROM citizens", conn)
payments_df = pd.read_sql_query("SELECT * FROM payments", conn)
courses_df = pd.read_sql_query("SELECT * FROM courses", conn)
conn.close()

st.markdown("<h3 style='color:#10B981; font-weight:800;'>📊 Сводные KPI экосистемы АПП СПб</h3>", unsafe_allow_html=True)
col_k1, col_k2, col_k3 = st.columns(3)

with col_k1:
    st.markdown(f'<div class="glass-card"><div class="card-title">Развернуто b2b-стандартов</div><div class="card-value">{len(courses_df)} моделей</div></div>', unsafe_allow_html=True)
with col_k2:
    st.markdown(f'<div class="glass-card"><div class="card-title">Зарегистрировано граждан</div><div class="card-value">{len(citizens_df)} анкет</div></div>', unsafe_allow_html=True)
with col_k3:
    total_rev = payments_df['amount'].sum() if not payments_df.empty else 0
    st.markdown(f'<div class="glass-card"><div class="card-title">Общая сумма привлеченных оплат</div><div class="card-value" style="color:#F59E0B;">{total_rev:,.0f} ₽</div></div>', unsafe_allow_html=True)

st.success("✓ Главный модуль успешно запущен. Переключитесь на нужный кабинет в левом меню сайдбара.")
