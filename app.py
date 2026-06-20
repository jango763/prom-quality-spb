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
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (БОРЬБА С RACE CONDITION И СБРОСОМ СЕССИИ)
# ==============================================================================
DB_NAME = "platform.db"

def init_db():
    """Инициализация единой общей базы данных для всех пользователей платформы"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица состояния заводов (баланс, премиум)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS factories (
            id TEXT PRIMARY KEY, balance REAL, is_premium INTEGER
        )
    """)
    # Таблица промышленных курсов ДПО
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, factory TEXT, clicks INTEGER, leads INTEGER, color TEXT
        )
    """)
    # Таблица b2b/b2c лидов соискателей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, course_title TEXT, status TEXT, rating TEXT
        )
    """)
    
    # Наполнение демо-данными при первом запуске
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

# ==============================================================================
# 3. БЕЗОПАСНЫЕ КОНТРОЛЛЕРЫ (ERROR BOUNDARY С TRY/EXCEPT)
# ==============================================================================
def get_factory_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM factories WHERE id='kirov_zavod'", conn)
        conn.close()
        if not df.empty:
            return True, df.iloc[0].to_dict()
        return False, "Завод не найден в базе данных"
    except Exception as e:
        return False, f"Ошибка чтения данных завода: {str(e)}"

def buy_lead_transaction(lead_id):
    """Безопасная b2b-транзакция списания средств за лид"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT balance, is_premium FROM factories WHERE id='kirov_zavod'")
        res = cursor.fetchone()
        balance, is_premium = res[0], res[1]
        
        if is_premium == 0 and balance < 500:
            conn.close()
            return False, "Недостаточно средств на балансе CPA. Пополните счет."
            
        if is_premium == 0:
            cursor.execute("UPDATE factories SET balance = balance - 500 WHERE id='kirov_zavod'")
            
        cursor.execute("UPDATE leads SET status = 'Разблокирован' WHERE id = ?", (lead_id,))
        conn.commit()
        conn.close()
        return True, "Контакт успешно выкуплен"
    except Exception as e:
        return False, f"Транзакция сорвана: {str(e)}"

def activate_premium_transaction():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE factories SET is_premium = 1 WHERE id='kirov_zavod'")
        conn.commit()
        conn.close()
        return True, "Безлимитный тариф активирован"
    except Exception as e:
        return False, f"Не удалось сменить тариф: {str(e)}"

def add_new_lead_from_student(course_title):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
        safe_phone = f"+7 (9xx) {random_digits[:3]}-{random_digits[3:5]}-{random_digits[5:]}"
        
        cursor.execute("""
            INSERT INTO leads (name, phone, course_title, status, rating) 
            VALUES (?, ?, ?, 'Заморожен', ?)
        """, (f"Выпускник академии №{random.randint(100, 999)}", safe_phone, course_title, f"⭐ {random.uniform(4.5, 5.0):.1f}"))
        cursor.execute("UPDATE courses SET leads = leads + 1 WHERE title = ?", (course_title,))
        conn.commit()
        conn.close()
        return True, "Лид сгенерирован"
    except Exception as e:
        return False, f"Ошибка генерации лида: {str(e)}"

# ==============================================================================
# 4. ИНТЕРФЕЙС И УПРАВЛЕНИЕ СЕССИЕЙ (Внутри st.session_state только кэш UI)
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

# Живые KPI подтягиваются из общей БД
conn = sqlite3.connect(DB_NAME)
total_leads_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM leads", conn).iloc[0]['cnt']
conn.close()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Подключено заводов СПб", value="142 предприятия", delta="+4 за неделю")
kpi2.metric(label="Граждан на обучении", value="482,900 чел.", delta="Охват регионов РФ")
kpi3.metric(label="Сгенерировано лидов (Общее)", value=f"{18410 + int(total_leads_count)} заявок", delta="Конверсия 91%")
kpi4.metric(label="Общий оборот эквайринга", value="4.2 млн ₽", delta="CPA модель")
st.write("---")

# ==============================================================================
# БИЗНЕС-ЛОГИКА РОЛЕЙ
# ==============================================================================
if user_role == "🏢 Предприятие / Завод (B2B)":
    st.subheader("📊 Мониторинг b2b-бюджета и цифрового кадрового следа")
    
    success, factory = get_factory_data()
    if not success:
        st.error(factory)
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric(label="Финтех-баланс (CPA)", value=f"{factory['balance']:,.2f} ₽")
        tariff_txt = "БЕЗЛИМИТ" if factory["is_premium"] == 1 else "CPA (500₽/лид)"
        c2.metric(label="Текущий B2B-тариф", value=tariff_txt)
        
        conn = sqlite3.connect(DB_NAME)
        leads_df = pd.read_sql_query("SELECT * FROM leads", conn)
        conn.close()
        
        c3.metric(label="Ваши целевые лиды", value=len(leads_df))
        
        if factory["is_premium"] == 0:
            if st.button("🔌 Переключить всю экосистему на Безлимитный Годовой Пакет", use_container_width=True, type="primary"):
                succ, err = activate_premium_transaction()
                if succ:
                    st.success(err)
                    st.rerun()
                else:
                    st.error(err)

        st.write("---")
        st.subheader("🎯 Поступившие горячие лиды из общей базы данных")
        
        if leads_df.empty:
            st.info("💡 На данный момент поступивших лидов нет.")
        else:
            for idx, row in leads_df.iterrows():
                with st.container(border=True):
                    st.markdown(f"**Курс:** {row['course_title']} | **Рейтинг:** {row['rating']}")
                    c_info, c_act = st.columns(2)
                    is_open = (factory["is_premium"] == 1) or (row["status"] == "Разблокирован")
                    c_info.write(f"**ФИО соискателя:** {row['name'] if is_open else '🔒 Скрыто системой CPA'}")
                    
                    if not is_open:
                        has_cash = factory["balance"] >= 500
                        btn_name = "💳 Открыть контакт (500 ₽)" if has_cash else "❌ Пополните счет"
                        if c_act.button(btn_name, key=f"fac_buy_{row['id']}_{idx}", use_container_width=True, disabled=not has_cash):
                            succ, err = buy_lead_transaction(row['id'])
