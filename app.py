import streamlit as st
import pandas as pd
import random
import sqlite3
import numpy as np
import io
import html

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И ЭКОСИСТЕМНЫЕ СТИЛИ (Айдентика АПП СПб)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема АПП", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #334155; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #10B981; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px; border-radius: 12px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; }
        .hero-title { font-size: 32px; font-weight: 800; }
        .hero-subtitle { font-size: 15px; color: #94A3B8; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: white; }
        .italy-box { padding: 20px; background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; color: #166534; margin-bottom: 20px; }
        .terminal-box { padding: 20px; background-color: #1E293B; color: #38BDF8; border-radius: 8px; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. БАЗОВЫЙ СЛОЙ ДАННЫХ (SQLite — Единый отказоустойчивый бэкенд)
# ==============================================================================
DB_NAME = "ecosystem.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Таблица заводов-производителей (Финтех балансы и пакеты продвижения)
    cursor.execute("CREATE TABLE IF NOT EXISTS factories (id TEXT PRIMARY KEY, name TEXT, balance REAL, is_premium INTEGER)")
    # Таблица развернутых курсов ДПО под конкретные модели станков
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, factory_id TEXT, title TEXT, equipment_model TEXT, 
            theory_text TEXT, clicks INTEGER, leads_generated INTEGER
        )
    """)
    # Таблица граждан РФ (Прогресс обучения и выходы на практику)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fio TEXT, phone TEXT, district TEXT, 
            active_course_id INTEGER, exam_score INTEGER, current_status TEXT
        )
    """)
    # Таблица глобальных настроек тизерного продвижения Ассоциации
    cursor.execute("CREATE TABLE IF NOT EXISTS marketing_hub (id TEXT PRIMARY KEY, headline TEXT, global_clicks INTEGER)")
    
    # Первичное наполнение системы под Демо-день
    cursor.execute("SELECT COUNT(*) FROM factories")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO factories VALUES ('kirov_zavod', 'АО «Кировский завод»', 25000.0, 0)")
        cursor.execute("INSERT INTO marketing_hub VALUES ('config', 'Самойлова Оксана подала в суд на Жигана потому что он тайно учился на ЧПУ!', 148200)")
        
        cursor.execute("""
            INSERT INTO courses (factory_id, title, equipment_model, theory_text, clicks, leads_generated) 
            VALUES ('kirov_zavod', 'Комплексная эксплуатация тяжелых токарных станков', 'ЧПУ серии ИТ-42 (стойка Syntec)', 
            'ИНСТРУКЦИЯ И СТАНДАРТ ПРОИЗВОДИТЕЛЯ:\nШаг 1. Проверить уровень масла в баке гидропривода.\nШаг 2. Загрузить карту нарезки в стойку Syntec.\nШаг 3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено во избежание поломки резца за 20 млн рублей.', 2850, 2)
        """)
        
        cursor.executemany("""
            INSERT INTO citizens (fio, phone, district, active_course_id, exam_score, current_status) VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("Никифоров А.В. (Выпускник СПбПУ)", "+7(921)555-44-33", "Кировский район", 1, 3, "Железный специалист"),
            ("Смирнов К.М. (Соискатель)", "+7(911)888-77-66", "Калининский район", 1, 3, "На практике")
        ])
    conn.commit()
    conn.close()

init_db()

# Контроллеры b2b/b2c логики
def get_factories_list():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM factories", conn)
    conn.close()
    return df

def get_courses_list():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM courses", conn)
    conn.close()
    return df

def get_citizens_list():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM citizens", conn)
    conn.close()
    return df

def get_marketing_headline():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT headline, global_clicks FROM marketing_hub WHERE id='config'").fetchone()
    conn.close()
    return res

def add_dpo_course(factory_id, title, equipment, text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (factory_id, title, equipment_model, theory_text, clicks, leads_generated) VALUES (?, ?, ?, ?, 0, 0)",
                   (factory_id, title, equipment, text))
    conn.commit()
    conn.close()

def update_marketing_headline(new_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE marketing_hub SET headline = ? WHERE id='config'", (new_text,))
    conn.commit()
    conn.close()

def simulate_teaser_click(course_id, volume):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE courses SET clicks = clicks + ? WHERE id = ?", (volume, course_id))
    cursor.execute("UPDATE marketing_hub SET global_clicks = global_clicks + ? WHERE id='config'", (volume,))
    conn.commit()
    conn.close()

def register_citizen_and_test(fio, phone, district, course_id, score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Жесткий фильтр: если 3 правильных ответа — допуск к практике, иначе — статус Обучение
    status = "Тест сдан. Ждет практику" if score == 3 else "Обучение"
    cursor.execute("""
        INSERT INTO citizens (fio, phone, district, active_course_id, exam_score, current_status) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fio, phone, district, course_id, score, status))
    if score == 3:
        cursor.execute("UPDATE courses SET leads_generated = leads_generated + 1 WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()

@st.cache_data(ttl=5)
def generate_excel_report(query_str):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query_str, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Аналитика_АПП')
    return output.getvalue()

# ==============================================================================
# 3. ЕДИНЫЙ ЭКОСИСТЕМНЫЙ ИНТЕРФЕЙС ПЛАТФОРМЫ
# ==============================================================================
with st.sidebar:
    st.title("🔒 Контур Доступа")
    current_cabinet = st.selectbox(
        "Выберите рабочее пространство:",
        ["🏢 Личный кабинет Производителя (B2B)", "🎓 Портал обучения Граждан РФ (B2C)", "🛠️ Наш кабинет АПП (Управление экосистемой)"]
    )
    st.write("---")
    st.caption("Официальный стек Ассоциации промышленных предприятий Санкт-Петербурга")

# Парадная экосистемная шапка
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
    </div>
""", unsafe_allow_html=True)

# Подтяжка живых KPI экосистемы для спонсоров
factories_df = get_factories_list()
courses_df = get_courses_list()
citizens_df = get_citizens_list()
headline_text, global_clicks_count = get_marketing_headline()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Производителей в системе", value=f"{len(factories_df)} заводов")
kpi2.metric(label="Развернутых курсов ДПО", value=f"{len(courses_df)} методик")
kpi3.metric(label="Граждан на платформе", value=f"{len(citizens_df)} соискателей")
kpi4.metric(label="Вирусный b2c-трафик (Охват)", value=f"{global_clicks_count:,} кликов")
st.write("---")

# ==============================================================================
# КАБИНЕТ 1: 🏢 ДЛЯ ПРОИЗВОДСТВЕННИКОВ (B2B-ВЫВОД МАТЕРИАЛОВ)
# ==============================================================================
if current_cabinet == "🏢 Личный кабинет Производителя (B2B)":
    st.header("🏢 Личный кабинет Завода-Производителя оборудования")
    
    st.markdown("""
        <div class="italy-box">
            <b>💡 Логика Итальянских Мастеров:</b> Выкладывайте развернутые обучающие материалы по вашим передовым станкам. 
            Граждане РФ обучатся работе именно на ваших технологиях, и придя на заводы страны, сформируют массовый b2b-спрос на закупку вашего оборудования.
        </div>
    """, unsafe_allow_html=True)
    
    tab_upload, tab_monitor = st.tabs(["📥 Внести и опубликовать ДПО курс", "📊 Мониторинг обученного персонала"])
    
    with tab_upload:
        st.subheader("Форма вывода развернутого учебного материала на рынок РФ")
        with st.form("course_upload_form"):
            c_title = st.text_input("Название программы обучения (например, Наладка токарных центров):")
            e_model = st.text_input("Модель вашего дорогостоящего станка/оборудования:", value="ЧПУ ИТ-42 (Syntec)")
            t_text = st.text_area("Развернутый пошаговый обучающий материал и правила безопасности:")
            
            if st.form_submit_button("Опубликовать курс в федеральный каталог", use_container_width=True):
                if c_title.strip() and e_model.strip() and t_text.strip():
