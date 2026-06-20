import streamlit as st
import pandas as pd
import random
import sqlite3
import numpy as np

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТИЛИ
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0284C7; }
        .highlight-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        .hero-banner { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 40px; border-radius: 16px; color: #FFFFFF; margin-bottom: 30px; border-left: 8px solid #0284C7; }
        .hero-title { font-size: 38px; font-weight: 800; color: #FFFFFF; margin-bottom: 5px; }
        .hero-subtitle { font-size: 18px; color: #94A3B8; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ
# ==============================================================================
DB_NAME = "platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS factories (id TEXT PRIMARY KEY, balance REAL, is_premium INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, factory TEXT, clicks INTEGER, leads INTEGER, color TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, course_title TEXT, status TEXT, rating TEXT)")
    
    cursor.execute("SELECT COUNT(*) FROM factories")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO factories VALUES ('kirov_zavod', 25000.0, 0)")
        cursor.executemany("INSERT INTO courses (title, factory, clicks, leads, color) VALUES (?, ?, ?, ?, ?)", [
            ("Отказоустойчивость гидравлических систем", "АО 'Силовые машины'", 1420, 84, "🔵"),
            ("Программирование ЧПУ циклов серии ИТ-42", "АО 'Кировский завод'", 2850, 196, "⚙️"),
            ("Метрология и лазерный контроль геометрии", "Обуховский завод", 930, 41, "🔬")
        ])
        cursor.executemany("INSERT INTO leads (name, phone, course_title, status, rating) VALUES (?, ?, ?, ?, ?)", [
            ("Александров К.М. (Военмех)", "+7 (921) 345-67-89", "Программирование ЧПУ циклов серии ИТ-42", "Заморожен", "⭐ 4.9"),
            ("Дмитриев А.В. (СПбПУ)", "+7 (911) 987-65-43", "Отказоустойчивость гидравлических систем", "Заморожен", "⭐ 4.7")
        ])
    conn.commit()
    conn.close()

init_db()

# Контроллеры
def get_factory_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM factories WHERE id='kirov_zavod'", conn)
        conn.close()
        if not df.empty:
            return True, df.iloc[0].to_dict()
        return False, "Завод не найден"
    except Exception as e:
        return False, str(e)

def buy_lead_transaction(lead_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT balance, is_premium FROM factories WHERE id='kirov_zavod'")
        balance, is_premium = cursor.fetchone()
        if is_premium == 0 and balance < 500:
            conn.close()
            return False, "Недостаточно средств"
        if is_premium == 0:
            cursor.execute("UPDATE factories SET balance = balance - 500 WHERE id='kirov_zavod'")
        cursor.execute("UPDATE leads SET status = 'Разблокирован' WHERE id = ?", (lead_id,))
        conn.commit()
        conn.close()
        return True, "Успешно"
    except Exception as e:
        return False, str(e)

def activate_premium_transaction():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE factories SET is_premium = 1 WHERE id='kirov_zavod'")
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
        cursor.execute("UPDATE courses SET leads = leads + 1 WHERE title = ?", (course_title,))
        conn.commit()
        conn.close()
        return True, "Успешно"
    except Exception as e:
        return False, str(e)

# ==============================================================================
# 3. УПРАВЛЕНИЕ ИНТЕРФЕЙСОМ
# ==============================================================================
if "active_course_id" not in st.session_state:
    st.session_state["active_course_id"] = None

with st.sidebar:
    st.title("ПромКачество")
    st.caption("Ассоциация промышленных предприятий СПб")
    st.write("---")
    user_role = st.selectbox(
        "⚡ Авторизация в контуре:",
        ["🏢 Предприятие / Завод (B2B)", "🎓 Гражданин / Ученик (B2C)", "💥 Маркетолог (Тизерный хаб)"]
    )

st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Цифровая экосистема «ПромКачество.СПб»</div>
        <div class="hero-subtitle">Федеральный каркас опережающего ДПО и автоматической лидогенерации АПП СПБ</div>
    </div>
""", unsafe_allow_html=True)

# FIX: Безопасный расчет KPI через .loc[0] вместо падающего .iloc['cnt']
conn = sqlite3.connect(DB_NAME)
total_leads_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM leads", conn).loc[0, 'cnt']
conn.close()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Подключено заводов СПб", value="142 предприятия", delta="+4 за неделю")
kpi2.metric(label="Граждан на обучении", value="482,900 чел.", delta="Охват регионов РФ")
kpi3.metric(label="Сгенерировано лидов (Общее)", value=f"{18410 + int(total_leads_count)} заявок", delta="Конверсия 91%")
kpi4.metric(label="Общий оборот эквайринга", value="4.2 млн ₽", delta="CPA модель")
st.write("---")

# ==============================================================================
# ОТРИСОВКА СТРАНИЦ В ЗАВИСИМОСТИ ОТ РОЛИ (СТРАНИЦЫ ТЕПЕРЬ СМЕНЯЮТСЯ ИДЕАЛЬНО)
# ==============================================================================
if user_role == "🏢 Предприятие / Завод (B2B)":
    st.subheader("🏢 Кабинет Индустриального Партнера")
    success, factory = get_factory_data()
    if success:
        c1, c2, c3 = st.columns(3)
        c1.metric(label="Финтех-баланс (CPA)", value=f"{factory['balance']:,.2f} ₽")
        tariff_txt = "БЕЗЛИМИТ" if factory["is_premium"] == 1 else "CPA (500₽/лид)"
        c2.metric(label="Текущий B2B-тариф", value=tariff_txt)
        
        conn = sqlite3.connect(DB_NAME)
        leads_df = pd.read_sql_query("SELECT * FROM leads", conn)
        conn.close()
        c3.metric(label="Ваши целевые лиды", value=len(leads_df))
        
        if factory["is_premium"] == 0:
            if st.button("🔌 Перейти на Безлимитный Годовой Пакет", use_container_width=True, type="primary"):
                succ, err = activate_premium_transaction()
                if succ: st.rerun()

        st.write("---")
        st.subheader("🎯 Поступившие горячие лиды")
        for idx, row in leads_df.iterrows():
            with st.container(border=True):
                st.markdown(f"**Курс:** {row['course_title']} | **Рейтинг:** {row['rating']}")
                c_info, c_act = st.columns(2)
                is_open = (factory["is_premium"] == 1) or (row["status"] == "Разблокирован")
                c_info.write(f"**ФИО соискателя:** {row['name'] if is_open else '🔒 Скрыто системой CPA'}")
                if not is_open:
                    has_cash = factory["balance"] >= 500
                    btn_name = "💳 Открыть контакт (500 ₽)" if has_cash else "❌ Пополните счет"
                    if c_act.button(btn_name, key=f"fac_buy_{row['id']}", use_container_width=True, disabled=not has_cash):
                        succ, err = buy_lead_transaction(row['id'])
                        if succ: st.rerun()
                else:
                    c_act.success(f"📞 {row['phone']}")

elif user_role == "🎓 Гражданин / Ученик (B2C)":
    st.subheader("🎓 Интерактивная академия профессиональной подготовки")
    
    st.write("📍 География промышленных мощностей")
    map_data = pd.DataFrame({'lat': [59.9004, 59.8821, 59.8341], 'lon': [30.4322, 30.2743, 30.4912]})
    st.map(map_data, size=40)

    st.write("---")
    conn = sqlite3.connect(DB_NAME)
    courses_df = pd.read_sql_query("SELECT * FROM courses", conn)
    conn.close()
    
    for idx, row in courses_df.iterrows():
        with st.container(border=True):
            col_icon, col_txt, col_btn = st.columns([1, 4, 2])
            col_icon.write(f"# {row['color']}")
            col_txt.write(f"### {row['title']}")
            col_txt.write(f"🏭 Индустриальный автор: **{row['factory']}**")
            
            if col_btn.button("🚀 Начать бесплатное обучение", key=f"stud_start_{row['id']}", use_container_width=True):
                st.session_state["active_course_id"] = row['id']
                succ, err = add_new_lead_from_student(row['title'])
                if succ: st.balloons(); st.rerun()
            
            if st.session_state["active_course_id"] == row['id']:
