import streamlit as st
import pandas as pd
import random
import sqlite3
import numpy as np
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И КОРПОРАТИВНЫЕ СТИЛИ (Промышленный дизайн)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0284C7; }
        .highlight-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .matching-box { padding: 15px; border-radius: 8px; background-color: #ECFDF5; border-left: 5px solid #10B981; color: #065F46; font-weight: 600; margin-bottom: 15px; }
        .hero-banner { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 40px; border-radius: 16px; color: #FFFFFF; margin-bottom: 30px; border-left: 8px solid #0284C7; }
        .hero-title { font-size: 34px; font-weight: 800; color: #FFFFFF; margin-bottom: 5px; }
        .hero-subtitle { font-size: 16px; color: #94A3B8; }
        .marketing-card { padding: 15px; background-color: #FFFBEB; border-left: 5px solid #F59E0B; border-radius: 4px; margin-bottom: 10px; }
        .factory-title { color: #1E293B; font-size: 24px; font-weight: 700; margin-bottom: 10px; }
        .preview-box { padding: 20px; background-color: #FEF2F2; border: 2px dashed #EF4444; border-radius: 12px; margin-top: 15px; }
        .passport-tag { display: inline-block; background-color: #E2E8F0; color: #334155; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 5px; margin-bottom: 5px; }
        .contract-signed { color: #10B981; font-weight: bold; font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (Общая база SQLite — Борьба с Race Condition)
# ==============================================================================
DB_NAME = "platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS factories (id TEXT PRIMARY KEY, balance REAL, is_premium INTEGER)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, course_title TEXT, 
            status TEXT, rating TEXT, district TEXT, current_status TEXT,
            skills_cnc TEXT, skills_cad TEXT, contract_status TEXT
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM factories")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO factories VALUES ('kirov_zavod', 25000.0, 0)")
        cursor.executemany("""
            INSERT INTO leads (name, phone, course_title, status, rating, district, current_status, skills_cnc, skills_cad, contract_status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ("Александров К.М. (Военмех)", "+7 (921) 345-67-89", "Цифровые стандарты безопасности «ПромКачество»", "Заморожен", "⭐ 4.9", "Кировский район", "Студент выпускного курса", "Fanuc (30ч)", "Компас-3D (95%)", "Подписан в ЭДО (отработка 3 года)"),
            ("Дмитриев А.В. (СПбПУ)", "+7 (911) 987-65-43", "Допуск к высокоточному измерительному оборудованию шеринг-хаба", "Заморожен", "⭐ 4.7", "Калининский район", "Выпускник колледжа/вуза", "Siemens (15ч)", "AutoCAD (88%)", "На согласовании")
        ])
    conn.commit()
    conn.close()

init_db()

# Данные промышленных гигантов из вашего ТЗ
factories_data = pd.DataFrame([
    {
        "name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район", "vacancies_count": 42,
        "vacancies_list": "• Оператор станков с ЧПУ\n• Слесарь-сборщик\n• Наладчик роботизированных комплексов",
        "description": "Ведущее машиностроительное предприятие России. Выпуск тракторов «Кировец», буровой техники и турбогенераторов.",
        "course": "Цифровые стандарты безопасности «ПромКачество»"
    },
    {
        "name": "ПАО «Силовые машины» (ЛМЗ)", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район", "vacancies_count": 38,
        "vacancies_list": "• Инженер-технолог по сварке\n• Токарь-карусельщик 5-6 разряда\n• Контролер ОТК",
        "description": "Крупнейшее в стране энергомашиностроительное предприятие. Производство мощных паровых, газовых и гидравлических турбин.",
        "course": "Допуск к высокоточному измерительному оборудованию шеринг-хаба"
    },
    {
        "name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район", "vacancies_count": 25,
        "vacancies_list": "• Монтажник электрооборудования летательных аппаратов\n• Испытатель двигателей\n• Оператор лазерных установок",
        "description": "Лидер авиационного двигателестроения. Разработка, производство и сервисное обслуживание вертолетных и самолетных двигателей.",
        "course": "Сертификация по строгим оборонным стандартам качества"
    }
])

# ==============================================================================
# 3. КЭШИРУЕМЫЙ СЛОЙ КОНТРОЛЛЕРОВ (ИСПРАВЛЕНИЕ БАГА #1 И #2)
# ==============================================================================
@st.cache_data(ttl=60)
def generate_excel_report(query):
    """ FIX #1: Энергонезависимый кэш генерации тяжелых Excel файлов """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='АПП_СПб_Отчет')
    return output.getvalue()

def check_phone_uniqueness(phone):
    """ FIX #2: Проверка телефона на уникальность для блокировки дубликатов """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM leads WHERE phone = ?", (phone,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def get_factory_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM factories WHERE id='kirov_zavod'", conn)
        conn.close()
        return (True, df.iloc.to_dict()) if not df.empty else (False, "Завод не найден")
    except Exception as e:
        return False, str(e)

def buy_lead_transaction(lead_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT balance, is_premium FROM factories WHERE id='kirov_zavod'")
        res = cursor.fetchone()
        if not res:
            conn.close()
            return False, "Завод не найден"
        balance, is_premium = res
        if is_premium == 1:
            cursor.execute("UPDATE leads SET status = 'Разблокирован' WHERE id = ?", (lead_id,))
            conn.commit()
            conn.close()
            return True, "Успешно"
        if balance < 500:
            conn.close()
            return False, "Недостаточно средств"
        cursor.execute("UPDATE factories SET balance = balance - 500 WHERE id='kirov_zavod'")
        cursor.execute("UPDATE leads SET status = 'Разблокирован' WHERE id = ?", (lead_id,))
        conn.commit()
        conn.close()
        return True, "Успешно"
    except Exception as e:
        return False, str(e)

def add_new_lead_from_student(name, phone, course_title, district, current_status, cnc_tag, cad_tag):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leads (name, phone, course_title, status, rating, district, current_status, skills_cnc, skills_cad, contract_status) 
            VALUES (?, ?, ?, 'Заморожен', ?, ?, ?, ?, ?, 'Подписан в ЭДО (отработка 3 года)')
        """, (name, phone, course_title, f"⭐ {random.uniform(4.5, 5.0):.1f}", district, current_status, cnc_tag, cad_tag))
        conn.commit()
        conn.close()
        return True, "Успешно"
    except Exception as e:
        return False, str(e)

# ==============================================================================
# 4. РЕНДЕРИНГ ИНТЕРФЕЙСА ПЛАТФОРМЫ
# ==============================================================================
with st.sidebar:
    st.title("Вход в систему")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        ["🏢 Для заводов и производств", "🎓 Для студентов и соискателей", "💥 Для маркетологов платформы"]
    )
    st.write("---")
    st.caption("Ассоциация промышленных предприятий СПб")

# Парадный индустриальный баннер
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Единая промышленная платформа «ПромКачество»</div>
        <div class="hero-subtitle">Система быстрого обучения кадров под нужды заводов Санкт-Петербурга</div>
    </div>
""", unsafe_allow_html=True)

# Живые b2b-метрики подтягиваются из общей БД
conn = sqlite3.connect(DB_NAME)
total_leads_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM leads", conn).loc[0, 'cnt']
unlocked_leads_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM leads WHERE status='Разблокирован'", conn).loc[0, 'cnt']
conn.close()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Заводов-партнеров в системе", value=f"{len(factories_data)} предприятия")
kpi2.metric(label="Студентов учатся сейчас", value="482,900 человек")
kpi3.metric(label="Всего подготовлено выпускников", value=f"{int(total_leads_count)} человек")
kpi4.metric(label="Подобрано сотрудников на заводы", value=f"{int(unlocked_leads_count)} человек")
st.write("---")

# --- ЛОГИКА: ЗАВОД (B2B) ---
if user_role == "🏢 Для заводов и производств":
    st.header("🏢 Кабинет отдела кадров предприятия")
    
