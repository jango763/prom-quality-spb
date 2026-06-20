import streamlit as st
import pandas as pd
import sqlite3
import io

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТРОГИЙ B2B-ДИЗАЙН
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Контур Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #334155; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0284C7; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px; border-radius: 12px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #EF4444; }
        .hero-title { font-size: 32px; font-weight: 800; }
        .hero-subtitle { font-size: 15px; color: #94A3B8; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: white; }
        .status-ready { background-color: #10B981; }
        .status-process { background-color: #3B82F6; }
        .status-warning { background-color: #F59E0B; }
        .simulator-term { padding: 20px; background-color: #1E293B; color: #38BDF8; border-radius: 8px; font-family: monospace; border-left: 5px solid #EF4444; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. СЛОЙ ДАННЫХ (SQLite Схема — СТРОГО ИЗ ДИРЕКТИВЫ)
# ==============================================================================
DB_NAME = "production_control.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Таблица курсов заводов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, factory_name TEXT, course_title TEXT, equipment_model TEXT, safety_instructions TEXT
        )
    """)
    # 2. Таблица пользователей / граждан РФ
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT, fio TEXT, phone TEXT, district TEXT, current_status TEXT
        )
    """)
    # 3. Таблица попыток сдачи тестов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, citizen_id INTEGER, course_id INTEGER, score INTEGER, is_passed TEXT
        )
    """)
    
    # Наполнение эталонными b2b-данными для Демо-дня
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions) VALUES (?, ?, ?, ?)",
                       ("АО «Кировский завод»", "Оператор токарных комплексов ЧПУ", "серия ИТ-42 (стойка Syntec)", 
                        "ИНСТРУКЦИЯ ПО БЕЗОПАСНОСТИ: 1. Перед запуском цикла нарезки ЧПУ ОБЯЗАТЕЛЬНО проверить давление в гидросистеме (норма 4.5-5.0 бар). 2. При аварийном росте давления немедленно активировать ручной сброс через клапан А-3. 3. Использование быстрого позиционирования G00 в зоне резания категорически запрещено — инструмент влетит в деталь."))
        
        cursor.execute("INSERT INTO citizens (fio, phone, district, current_status) VALUES (?, ?, ?, ?)",
                       ("Иванов Иван Игоревич", "+7(921)333-22-11", "Кировский район", "Железный специалист"))
        cursor.execute("INSERT INTO citizens (fio, phone, district, current_status) VALUES (?, ?, ?, ?)",
                       ("Петров Пётр Сергеевич", "+7(911)444-55-66", "Калининский район", "На практике"))
        
        cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (1, 1, 3, 'True')")
        cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (2, 1, 3, 'True')")
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# 3. СЛОЙ ЖЕЛЕЗНОЙ ЛОГИКИ (4 Функции Управления)
# ==============================================================================
def add_dpo_course(factory, title, equipment, text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions) VALUES (?, ?, ?, ?)",
                   (factory, title, equipment, text))
    conn.commit()
    conn.close()

def submit_test_results(citizen_id, course_id, correct_answers, user_answers):
    """ Проверяет тест. Если есть ХОТЬ ОДНА ошибка — допуск закрыт """
    is_passed = "True"
    score = 0
    for q in correct_answers:
        if user_answers.get(q) == correct_answers[q]:
            score += 1
        else:
            is_passed = "False" # Хоть одна ошибка — провал!
            
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_attempts (citizen_id, course_id, score, is_passed) VALUES (?, ?, ?, ?)",
                   (citizen_id, course_id, score, is_passed))
    
    # Меняем статус гражданина
    new_status = "Тест сдан. Ждет практику" if is_passed == "True" else "Обучение"
    cursor.execute("UPDATE citizens SET current_status = ? WHERE id = ?", (new_status, citizen_id))
    conn.commit()
    conn.close()
    return is_passed == "True"

def enroll_to_practice(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'На практике' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

def approve_specialist(citizen_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE citizens SET current_status = 'Железный專员' WHERE id = ?", (citizen_id,)) # Ошибка локализации, исправим на 'Железный специалист' ниже
    cursor.execute("UPDATE citizens SET current_status = 'Железный специалист' WHERE id = ?", (citizen_id,))
    conn.commit()
    conn.close()

@st.cache_data(ttl=10)
def build_hr_excel():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("""
        SELECT c.fio as 'ФИО Мастера', c.phone as 'Телефон', c.district as 'Район проживания', crs.equipment_model as 'Аттестованный станок'
        FROM citizens c
        JOIN test_attempts ta ON c.id = ta.citizen_id
        JOIN courses crs ON ta.course_id = crs.id
        WHERE c.current_status = 'Железный специалист' AND ta.is_passed = 'True'
    """, conn)
    conn.close()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Проверенные_Мастера')
    return output.getvalue()

# ==============================================================================
# 4. СЛОЙ ИНТЕРФЕЙСА (views.py — СТРОГО ПО ТЗ)
# ==============================================================================
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная система контроля квалификации ОПК СПб</div>
        <div class="hero-subtitle">Защищенный b2b/b2c-контур Ассоциации промышленных предприятий Санкт-Петербурга</div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ Контроль Доступов")
    user_role = st.selectbox("Авторизация в системе:", ["🏢 Личный кабинет Производственника", "🎓 Портал Гражданина РФ"])

# --- ВКЛАДКА 1: КАБИНЕТ ПРОИЗВОДСТВЕННИКА ---
if user_role == "🏢 Личный кабинет Производственника":
    st.header("🏢 Управление кадровым допуском предприятия")
    
    # Проводка 1: Форма загрузки ДПО курсов
    st.subheader("📥 Ввод новых стандартов и регламентов оборудования")
    with st.form("add_dpo_form"):
        f_name = st.text_input("Название вашего предприятия:", value="АО «Кировский завод»")
        c_title = st.text_input("Название технического курса подготовки:")
        e_model = st.text_input("Модель дорогостоящего промышленного оборудования (Станка):", value="Syntec серии ИТ-42")
        s_text = st.text_area("Текст жесткого регламента техники безопасности:")
        
        if st.form_submit_button("Опубликовать курс для граждан РФ", use_container_width=True):
            if c_title.strip() and s_text.strip():
                add_dpo_course(f_name, c_title, e_model, s_text)
                st.success("Новый регламент безопасности успешно выведен на платформу!")
            else:
                st.error("Заполните все поля формы!")

    st.write("---")
    
    # Проводка 2: Реестр проверенных специалистов и скачивание Excel
    col_head, col_excel = st.columns(2)
    col_head.subheader("🎯 Реестр HR-отдела: Верифицированные кадры")
    
    excel_bytes = build_hr_excel()
    col_excel.download_button(
        label="📥 Скачать список проверенных мастеров в Excel", data=excel_bytes,
        file_name="Реестр_Железных_Специалистов.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True
    )
    
    conn = sqlite3.connect(DB_NAME)
    all_citizens = pd.read_sql_query("SELECT id, fio, phone, district, current_status FROM citizens", conn)
    conn.close()
    
    st.info("В реестр выводятся только соискатели, успешно сдавшие тест ТБ и подтвержденные мастером цеха.")
    for idx, c_row in all_citizens.iterrows():
        with st.container(border=True):
            col_data, col_master_action = st.columns([3, 1])
            
            # Рендеринг красивых статусов
            st_badge = ""
            if c_row['current_status'] == "Железный специалист":
                st_badge = '<span class="status-badge status-ready">✓ Железный специалист</span>'
            elif c_row['current_status'] == "На практике":
                st_badge = '<span class="status-badge status-process">⚙️ На практике</span>'
            elif c_row['current_status'] == "Тест сдан. Ждет практику":
