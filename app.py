import streamlit as st
import pandas as pd
import sqlite3
import io

# 1. НАСТРОЙКА СТРАНИЦЫ И СТИЛЕЙ
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# Прячем стандартные ошибки Streamlit для продакшена
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    th { background-color: #f0f2f6 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. ИНИЦИАЛИЗАЦИЯ И СВЯЗЬ С БАЗОЙ ДАННЫХ (БЕЗ RACE CONDITION)
def get_db_connection():
    # Включаем таймаут и режим WAL для многопоточной работы соискателей и заводов
    conn = sqlite3.connect("prom_quality.db", timeout=20)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db_connection() as conn:
        # Таблица курсов ДПО от заводов
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factory_name TEXT,
                course_title TEXT,
                equipment_model TEXT,
                safety_instructions TEXT
            )
        """)
        # Таблица граждан РФ (соискателей)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS citizens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fio TEXT,
                phone TEXT UNIQUE,
                district TEXT,
                current_status TEXT,
                assigned_course_id INTEGER,
                FOREIGN KEY(assigned_course_id) REFERENCES courses(id) ON DELETE SET NULL
            )
        """)
        conn.commit()
        
        # Наполняем демо-данными, если база пустая
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        if cursor.fetchone()[0] == 0:
            conn.execute("""
                INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions)
                VALUES 
                ('АО «Кировский завод»', 'Оператор станков с ЧПУ', 'Токарный комплекс ЧПУ (20млн+)', 'РЕГЛАМЕНТ: При аварийной остановке шпинделя немедленно нажмите красную кнопку аварийного стопа (E-STOP). Запрещено открывать защитный кожух до полной остановки суппорта. Давление в гидросистеме не должно превышать 4.5 МПа.'),
                ('ПАО «Силовые машины»', 'Токарь-карусельщик 5-6 разряда', 'Карусельный станок тяжелого гидростроения', 'РЕГЛАМЕНТ: Перед запуском планшайбы убедитесь в надежной фиксации заготовки b2b-крановыми захватами. Запрещено находиться в зоне вращения деталей диаметром более 2000 мм без защитного экрана.'),
                ('ОАО «ОДК-Климов»', 'Оператор лазерных установок', 'Роботизированный лазерный комплекс', 'РЕГЛАМЕНТ: Работа строго в защитных очках спектра 1064 нм. Перед началом резки проверить герметичность оптического тракта и подачу защитного газа (аргон). Дефекты линзы ведут к порче лазерной головки.')
            """)
            conn.commit()

init_db()

# 3. ЕДИНЫЙ ВЕРХНИЙ КОНТРОЛЛЕР РОЛЕЙ (РАЗВЕДЕНИЕ ПОЛЬЗОВАТЕЛЕЙ)
st.sidebar.title("🛡️ Панель управления")
current_role = st.sidebar.selectbox(
    "Выберите вашу роль в экосистеме:",
    ["🤖 Главная страница / Карта", "🏢 Личный кабинет Производственника (B2B)", "🎓 Портал Гражданина РФ (B2C)"]
)

# ----------------------------------------------------------------------------------------------------------------------
# ЭКРАН 1: ГЛАВНАЯ СТРАНИЦА И ИНТЕРАКТИВНАЯ КАРТА
# ----------------------------------------------------------------------------------------------------------------------
if current_role == "🤖 Главная страница / Карта":
    st.title("🏭 Единая промышленная платформа «ПромКачество»")
    st.caption("Система быстрого обучения кадров под нужды заводов Санкт-Петербурга")
    
    # Метрики вовлеченности
    m1, m2, m3 = st.columns(3)
    m1.metric("Заводов-партнеров", "142 предприятия")
    m2.metric("Студентов учатся сейчас", "482,900 человек")
    with get_db_connection() as conn:
        ready_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='Железный специалист'").fetchone()[0]
    m3.metric("Подготовлено железных специалистов", f"{ready_count} чел.")
    
    st.write("---")
    st.subheader("📍 Посмотрите, где находятся заводы-работодатели на карте города")
    st.info("💡 Выберите предприятие из списка ниже, чтобы сфокусировать карту и открыть активные вакансии.")
    
    # Гео-модель
    factories_geo = pd.DataFrame([
        {"name": "АО «Кировский завод»", "lat": 59.8789, "lon": 30.2644, "district": "Кировский район"},
        {"name": "ПАО «Силовые машины»", "lat": 59.9572, "lon": 30.3842, "district": "Калининский район"},
        {"name": "ОАО «ОДК-Климов»", "lat": 60.0247, "lon": 30.3015, "district": "Приморский район"}
    ])
    
    selected_factory = st.selectbox("Выберите завод для изучения:", ["Все заводы"] + list(factories_geo["name"]))
    
    if selected_factory == "Все заводы":
        st.map(factories_geo, zoom=10, use_container_width=True)
    else:
        filtered_geo = factories_geo[factories_geo["name"] == selected_factory]
        st.map(filtered_geo, zoom=12, use_container_width=True)
        
        # Подгружаем информацию по заводу из БД
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            course_data = conn.execute("SELECT * FROM courses WHERE factory_name=?", (selected_factory,)).fetchone()
        
        if course_data:
            st.markdown(f"### 🏢 Профиль предприятия: {selected_factory}")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Целевое оборудование:** `{course_data['equipment_model']}`")
                st.markdown(f"**Расположение производственной площадки:** {filtered_geo['district'].values[0]}")
            with c2:
                st.markdown(f"**Доступная программа подготовки:** {course_data['course_title']}")
                if st.button("🚀 Начать подготовку под этот стандарт", type="primary", use_container_width=True):
                    st.success("Перейдите во вкладку 'Портал Гражданина РФ' в левом меню для регистрации и сдачи экзамена.")

# ----------------------------------------------------------------------------------------------------------------------
# ЭКРАН 2: ЛИЧНЫЙ КАБИНЕТ ПРОИЗВОДСТВЕННИКА (B2B)
# ----------------------------------------------------------------------------------------------------------------------
elif current_role == "🏢 Личный кабинет Производственника (B2B)":
    st.title("🏢 Кабинет отдела кадров и главного инженера")
    st.write("Управление образовательными стандартами ДПО и наем сертифицированных кадров.")
    
    tab_add, tab_hr = st.tabs(["✍️ Загрузить программу ДПО", "📥 Реестр готовых специалистов"])
    
    with tab_add:
        st.subheader("Форма добавления регламента обучения для нового станка")
        with st.form("add_course_form", clear_on_submit=True):
            f_name = st.selectbox("Ваше предприятие:", ["АО «Кировский завод»", "ПАО «Силовые машины»", "ОАО «ОДК-Климов»"])
            c_title = st.text_input("Название программы обучения (например, Оператор фрезерного комплекса):")
            e_model = st.text_input("Модель и стоимость станка (например, DMG MORI CTX 20млн+):")
            s_text = st.text_area("Жесткий технический регламент безопасности (Текст инструкции):")
            
            submit_course = st.form_submit_button("Опубликовать стандарт ДПО")
            if submit_course:
                if f_name and c_title.strip() and e_model.strip() and s_text.strip():
                    with get_db_connection() as conn:
                        conn.execute("""
                            INSERT INTO courses (factory_name, course_title, equipment_model, safety_instructions)
                            VALUES (?, ?, ?, ?)
                        """, (f_name, c_title.strip(), e_model.strip(), s_text.strip()))
                        conn.commit()
                    st.success(f"✅ Программа '{c_title}' успешно добавлена в общую базу данных платформы.")
                    st.cache_data.clear()
                else:
                    st.error("❌ Заполните все поля! Промышленный регламент не терпит пустых данных.")
                    
    with tab_hr:
        st.subheader("📋 Соискатели, успешно сдавшие тест и практику без поломок оборудования")
        
        with get_db_connection() as conn:
            query = """
                SELECT c.fio, c.phone, c.district, c.current_status, co.factory_name, co.equipment_model 
                FROM citizens c
                JOIN courses co ON c.assigned_course_id = co.id
                WHERE c.current_status = 'Железный специалист'
            """
            hr_df = pd.read_sql_query(query, conn)
            
        if hr_df.empty:
            st.info("💡 На данный момент готовых специалистов нет. Пройдите обучение во вкладке соискателя, чтобы сгенерировать кадры.")
        else:
            # Красивое переименование для HR-отдела
            hr_df.columns = ["ФИО соискателя", "Контактный телефон", "Район проживания", "Статус квалификации", "Завод аттестации", "Допуск к оборудованию"]
            st.dataframe(hr_df, use_container_width=True, hide_index=True)
            
            # Контекстный менеджер для чистой выгрузки в Excel в один клик
            with io.BytesIO() as buffer:
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    hr_df.to_excel(writer, index=False, sheet_name="Специалисты")
                excel_bytes = buffer.getvalue()
                
            st.download_button(
                label="📥 Скачать чистый реестр кандидатов в Excel для HR",
                data=excel_bytes,
                file_name="validated_prom_specialists.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

