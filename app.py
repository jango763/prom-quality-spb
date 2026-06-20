import streamlit as st
import pandas as pd
import random
import sqlite3
import numpy as np
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И ЭКОСИСТЕМНЫЕ СТИЛИ (Дизайн Сбера/Яндекса)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0284C7; }
        .hero-banner { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 40px; border-radius: 16px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; }
        .hero-title { font-size: 34px; font-weight: 800; color: #FFFFFF; margin-bottom: 5px; }
        .hero-subtitle { font-size: 16px; color: #94A3B8; }
        .simulator-box { padding: 25px; background-color: #1E293B; color: #F8FAFC; border-radius: 12px; font-family: 'Courier New', Courier, monospace; border-left: 6px solid #38BDF8; margin-top: 15px; }
        .passport-tag { display: inline-block; background-color: #E2E8F0; color: #334155; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; margin-right: 5px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (SQLite БД — Единый отказоустойчивый контур)
# ==============================================================================
DB_NAME = "platform.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS factories (id TEXT PRIMARY KEY, balance REAL, is_premium INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS marketing_stats (id TEXT PRIMARY KEY, clicks INTEGER, views INTEGER)")
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
        cursor.execute("INSERT INTO marketing_stats VALUES ('global', 5200, 482900)")
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

# Базовые данные промышленных гигантов (Модель)
factories_data = pd.DataFrame([
    {
        "name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район", "vacancies_count": 42,
        "vacancies_list": "• Оператор станков с ЧПУ\n• Слесарь-сборщик\n• Наладчик роботизированных комплексов",
        "description": "Ведущее машиностроительное предприятие России. Выпуск тракторов «Кировец», буровой техники и турбогенераторов.",
        "course": "Цифровые стандарты безопасности «ПромКачество»", "color": "⚙️"
    },
    {
        "name": "ПАО «Силовые машины» (ЛМЗ)", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район", "vacancies_count": 38,
        "vacancies_list": "• Инженер-технолог по сварке\n• Токарь-карусельщик 5-6 разряда\n• Контролер ОТК",
        "description": "Крупнейшее в стране энергомашиностроительное предприятие. Производство мощных паровых, газовых и гидравлических турбин.",
        "course": "Допуск к высокоточному измерительному оборудованию шеринг-хаба", "color": "🔵"
    },
    {
        "name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район", "vacancies_count": 25,
        "vacancies_list": "• Монтажник электрооборудования летательных аппаратов\n• Испытатель двигателей\n• Оператор лазерных установок",
        "description": "Лидер авиационного двигателестроения. Разработка, производство и сервисное обслуживание вертолетных и самолетных двигателей.",
        "course": "Сертификация по строгим оборонным стандартам качества", "color": "🔬"
    }
])

# Контроллеры b2b-логики
def get_factory_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM factories WHERE id='kirov_zavod'", conn)
    conn.close()
    if not df.empty:
        return df.loc[0].to_dict()
    return {"balance": 0.0, "is_premium": 0}

def get_marketing_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM marketing_stats WHERE id='global'", conn)
    conn.close()
    if not df.empty:
        return df.loc[0].to_dict()
    return {"clicks": 0, "views": 0}

def add_new_lead_from_student(name, phone, course_title, district, current_status, cnc_tag, cad_tag):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads (name, phone, course_title, status, rating, district, current_status, skills_cnc, skills_cad, contract_status) 
        VALUES (?, ?, ?, 'Заморожен', ?, ?, ?, ?, ?, 'Подписан в ЭДО (отработка 3 года)')
    """, (name, phone, course_title, f"⭐ {random.uniform(4.5, 5.0):.1f}", district, current_status, cnc_tag, cad_tag))
    cursor.execute("UPDATE marketing_stats SET clicks = clicks + 1 WHERE id='global'")
    conn.commit()
    conn.close()

@st.cache_data(ttl=10)
def generate_excel_report(query):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Экспорт_ПромКачество')
    return output.getvalue()

# ==============================================================================
# 3. НАВИГАЦИЯ (САЙДБАР)
# ==============================================================================
with st.sidebar:
    st.title("Вход в систему")
    user_role = st.selectbox(
        "Выберите ваш личный кабинет:",
        ["🏢 Для заводов и производств", "🎓 Для студентов и соискателей", "💥 Для маркетологов платформы"]
    )
    st.write("---")
    st.caption("🛡️ Защищенный b2b/b2c контур АПП СПб")

# Парадный индустриальный баннер АПП СПБ
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Единая промышленная платформа «ПромКачество»</div>
        <div class="hero-subtitle">Интерактивный b2b/b2c-каркас опережающего ДПО под нужды ОПК Санкт-Петербурга</div>
    </div>
""", unsafe_allow_html=True)

# Живые b2b-метрики подтягиваются из общей БД
conn = sqlite3.connect(DB_NAME)
total_leads_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM leads", conn).loc[0, 'cnt']
unlocked_leads_count = pd.read_sql_query("SELECT COUNT(*) as cnt FROM leads WHERE status='Разблокирован'", conn).loc[0, 'cnt']
conn.close()

m_stats = get_marketing_data()

# Создаем ИНТЕРАКТИВНЫЕ карточки-кнопки
if "active_kpi_tab" not in st.session_state:
    st.session_state["active_kpi_tab"] = None

k_col1, k_col2, k_col3, k_col4 = st.columns(4)

with k_col1:
    if st.button(f"🏢 Заводов в системе\n\n {len(factories_data)} предприятий", use_container_width=True):
        st.session_state["active_kpi_tab"] = "factories"
with k_col2:
    if st.button(f"🎓 Студентов учатся\n\n {m_stats['views']:,} человек", use_container_width=True):
        st.session_state["active_kpi_tab"] = "students"
with k_col3:
    if st.button(f"📝 Всего выпускников\n\n {int(total_leads_count)} человек", use_container_width=True):
        st.session_state["active_kpi_tab"] = "leads"
with k_col4:
    if st.button(f"🤝 Подобрано сотрудников\n\n {int(unlocked_leads_count)} человек", use_container_width=True):
        st.session_state["active_kpi_tab"] = "hired"

# РЕНДЕРИНГ ДИНАМИЧЕСКИХ ДАННЫХ ПРИ КЛИКЕ НА KPI КАРТОЧКИ
if st.session_state["active_kpi_tab"] == "factories":
    st.info("📊 Распределение индустриальных партнеров АПП по районам Санкт-Петербурга:")
    st.dataframe(factories_data[['name', 'district', 'vacancies_count']], use_container_width=True, hide_index=True)
elif st.session_state["active_kpi_tab"] == "students":
    st.info("📈 Статистика вовлечения соискателей в режиме реального времени:")
    chart_data = pd.DataFrame(np.random.randn(15, 2), columns=['Просмотры тизеров', 'Переходы в симулятор']).cumsum()
    st.line_chart(chart_data)
elif st.session_state["active_kpi_tab"] == "leads":
    st.info("🏆 Стена славы выпускников: соискатели, успешно сдавшие технический экзамен:")
    conn = sqlite3.connect(DB_NAME)
    leads_view = pd.read_sql_query("SELECT name, course_title, rating, current_status FROM leads", conn)
    conn.close()
    st.dataframe(leads_view, use_container_width=True, hide_index=True)
elif st.session_state["active_kpi_tab"] == "hired":
    st.success(f"💳 Коммерческий успех платформы: {int(unlocked_leads_count)} прямых b2b-контрактов заключено через систему CPA.")

st.write("---")

# ==============================================================================
# --- ИНТЕРФЕЙС: ЗАВОД (B2B) ---
# ==============================================================================
