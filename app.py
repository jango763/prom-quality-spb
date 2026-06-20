import streamlit as st
import pandas as pd
import random
import sqlite3
import numpy as np

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И КОРПОРАТИВНЫЕ СТИЛИ
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0284C7; }
        .highlight-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .hero-banner { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 40px; border-radius: 16px; color: #FFFFFF; margin-bottom: 30px; border-left: 8px solid #0284C7; }
        .hero-title { font-size: 34px; font-weight: 800; color: #FFFFFF; margin-bottom: 5px; }
        .hero-subtitle { font-size: 16px; color: #94A3B8; }
        .marketing-card { padding: 15px; background-color: #FFFBEB; border-left: 5px solid #F59E0B; border-radius: 4px; margin-bottom: 10px; }
        .factory-title { color: #1E293B; font-size: 24px; font-weight: 700; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (SQLite БД — Единое b2b-хранилище)
# ==============================================================================
DB_NAME = "platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS factories (id TEXT PRIMARY KEY, balance REAL, is_premium INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, course_title TEXT, status TEXT, rating TEXT)")
    
    cursor.execute("SELECT COUNT(*) FROM factories")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO factories VALUES ('kirov_zavod', 1500.0, 0)")
        cursor.executemany("INSERT INTO leads (name, phone, course_title, status, rating) VALUES (?, ?, ?, ?, ?)", [
            ("Александров К.М. (Военмех)", "+7 (921) 345-67-89", "Цифровые стандарты безопасности «ПромКачество»", "Заморожен", "⭐ 4.9"),
            ("Дмитриев А.В. (СПбПУ)", "+7 (911) 987-65-43", "Допуск к высокоточному измерительному оборудованию шеринг-хаба", "Заморожен", "⭐ 4.7")
        ])
    conn.commit()
    conn.close()

init_db()

# Данные для карты и b2b-профилей из вашего ТЗ
factories_data = pd.DataFrame([
    {
        "name": "АО «Кировский завод»",
        "latitude": 59.8789,
        "longitude": 30.2644,
        "district": "Кировский район",
        "vacancies_count": 42,
        "vacancies_list": "• Оператор станков с ЧПУ\n• Слесарь-сборщик\n• Наладчик роботизированных комплексов",
        "description": "Ведущее машиностроительное предприятие России. Выпуск тракторов «Кировец», буровой техники и турбогенераторов. Модернизированное b2b-производство полного цикла.",
        "course": "Цифровые стандарты безопасности «ПромКачество»"
    },
    {
        "name": "ПАО «Силовые машины» (ЛМЗ)",
        "latitude": 59.9572,
        "longitude": 30.3842,
        "district": "Калининский район",
        "vacancies_count": 38,
        "vacancies_list": "• Инженер-технолог по сварке\n• Токарь-карусельщик 5-6 разряда\n• Контролер ОТК",
        "description": "Крупнейшее в стране энергомашиностроительное предприятие. Производство мощных паровых, газовых и гидравлических турбин для ТЭС, АЭС и ГЭС.",
        "course": "Допуск к высокоточному измерительному оборудованию шеринг-хаба"
    },
    {
        "name": "ОАО «ОДК-Климов»",
        "latitude": 60.0247,
        "longitude": 30.3015,
        "district": "Приморский район",
        "vacancies_count": 25,
        "vacancies_list": "• Монтажник электрооборудования летательных аппаратов\n• Испытатель двигателей\n• Оператор лазерных установок",
        "description": "Лидер авиационного двигателестроения. Разработка, производство и сервисное обслуживание вертолетных и самолетных двигателей. Высокотехнологичные чистые зоны.",
        "course": "Сертификация по строгим оборонным стандартам качества"
    }
])

# Контроллеры b2b-логики
def get_factory_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM factories WHERE id='kirov_zavod'", conn)
        conn.close()
        return (True, df.iloc[0].to_dict()) if not df.empty else (False, "Завод не найден")
    except Exception as e:
        return False, str(e)

def update_factory_balance(amount):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE factories SET balance = balance + ? WHERE id='kirov_zavod'", (amount,))
        conn.commit()
        conn.close()
        return True, "Успешно"
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

def add_new_lead_from_student(course_title):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
        safe_phone = f"+7 (931) {random_digits[:3]}-{random_digits[3:5]}-{random_digits[5:]}"
        cursor.execute("INSERT INTO leads (name, phone, course_title, status, rating) VALUES (?, ?, ?, 'Заморожен', ?)",
                       (f"Выпускник академии №{random.randint(100, 999)}", safe_phone, course_title, f"⭐ {random.uniform(4.5, 5.0):.1f}"))
        conn.commit()
        conn.close()
        return True, "Успешно"
    except Exception as e:
        return False, str(e)

# ==============================================================================
# 3. НАВИГАЦИЯ И АВТОРИЗАЦИЯ
# ==============================================================================
if "active_course_title" not in st.session_state:
    st.session_state["active_course_title"] = None

with st.sidebar:
    st.title("Вход в систему")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        ["🏢 Для заводов и производств", "🎓 Для студентов и соискателей", "💥 Для маркетологов платформы"]
    )
    st.write("---")
    st.caption("Ассоциация промышленных предприятий Санкт-Петербурга")

# Парадный индустриальный баннер АПП СПБ
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Единая промышленная платформа «ПромКачество»</div>
        <div class="hero-subtitle">Система быстрого обучения кадров под нужды заводов Санкт-Петербурга</div>
    </div>
""", unsafe_allow_html=True)

# Живые b2b-метрики из базы данных
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

# ==============================================================================
# 4. ОТРИСОВКА ИНТЕРФЕЙСОВ РОЛЕЙ
# ==============================================================================

# --- ИНТЕРФЕЙС: ЗАВОД (B2B) ---
if user_role == "🏢 Для заводов и производств":
    st.header("🏢 Кабинет отдела кадров предприятия")
    st.write("Здесь вы управляете бюджетом на подбор персонала и видите анкеты людей, которые обучились по вашим инструкциям.")
    
    success, factory = get_factory_data()
    if success:
        c1, c2, c3 = st.columns(3)
        c1.metric(label="Ваш остаток на счете подбора", value=f"{factory['balance']:,.2f} ₽")
        tariff_txt = "БЕЗЛИМИТНЫЙ ГОДОВОЙ НАЙМ" if factory["is_premium"] == 1 else "🪙 Поштучный подбор (500₽ / анкета)"
        c2.metric(label="Ваш текущий тариф", value=tariff_txt)
        
        conn = sqlite3.connect(DB_NAME)
        leads_df = pd.read_sql_query("SELECT * FROM leads", conn)
        conn.close()
        c3.metric(label="Готовых кандидатов в базе", value=len(leads_df))

        # ИСПРАВЛЕННЫЙ ПУЛЬТ УПРАВЛЕНИЯ БЮДЖЕТОМ (СТРОГО СОБЛЮДЕНЫ ОТСТУПЫ В КНОПКАХ)
        st.write("---")
        st.subheader("⚙️ Панель управления b2b-бюджетом завода")
        col_pay, col_tariff = st.columns(2)
        
        with col_pay:
            st.markdown("**💰 Имитация пополнения счета подбора:**")
            deposit_amount = st.number_input("Введите сумму пополнения (₽):", min_value=1000, max_value=500000, value=10000, step=5000)
