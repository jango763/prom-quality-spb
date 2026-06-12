import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ================= АРХИТЕКТУРА ИНИЦИАЛИЗАЦИИ БАЗЫ ДАННЫХ =================
def init_db():
    with sqlite3.connect('prom_quality.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                specialization TEXT,
                target_factory TEXT,
                match_rate INTEGER,
                timestamp TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lab_bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                lab_name TEXT,
                hours_requested INTEGER,
                total_cost INTEGER,
                timestamp TEXT
            )
        ''')
        conn.commit()

init_db()

# Настройка B2B-страницы ПромКачество.СПб
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

st.title("Экосистема «ПромКачество.СПб»")
st.caption("Флагманский b2b/b2c-прототип платформы для Ассоциации промышленных производств")

# Боковое меню выбора концепций
option = st.sidebar.radio(
    "Выберите вариант концепции для демонстрации:",
    ("Вариант 1: Кадровый хаб (Mэтчинг Яндекса)", 
     "Вариант 2: Шеринг-экономика & R&D (Арбитраж Авито)", 
     "Вариант 3: Финтех-Навигатор образования (Экосистема Сбера)",
     "📊 Панель Управления Ассоциации (Аудит БД)")
)

# ================= ВАРИАНТ 1: КАДРОВЫЙ ХАБ =================
if option == "Вариант 1: Кадровый хаб (Mэтчинг Яндекса)":
    st.header("🎯 Концепт: Умный b2b-мэтчинг и Цифровой след выпускника")
    st.write("Интеллектуальный подбор молодых специалистов под нужды оборонно-промышленного комплекса СПб.")
    
    students_db = {
        "Иванов И. И. (Политех)": {"spec": "Робототехника и АСУ ТП", "qa": 4.9, "skills": ["ПЛК", "КОМПАС-3D", "C++"]},
        "Петров А. С. (ИТМО)": {"spec": "Лазерные технологии", "qa": 4.7, "skills": ["Оптика", "CNC-станки", "Python"]},
        "Сидоров К. М. (ЛЭТИ)": {"spec": "Микроэлектроника", "qa": 4.5, "skills": ["Чистые помещения", "VHDL", "Altium"]}
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👤 Выберите соискателя из базы вузов:")
        selected_student = st.selectbox("Студенты, прошедшие QA-верификацию Ассоциации:", list(students_db.keys()))
        
        student_data = students_db[selected_student]
        st.info(f"**Специализация:** {student_data['spec']}\n\n**Внутренний рейтинг QA:** ⭐️ {student_data['qa']} / 5.0")
        st.success(f"Verified Skills: {', '.join(student_data['skills'])}")
    
    with col2:
        st.subheader("🏭 Выберите целевое предприятие:")
        factory = st.selectbox("Заводы со свободными b2b-вакансиями:", ["Кировский завод", "ОАО Завод Арсенал", "ОДК-Климов"])
        
        match_rate = 95 if "Кировский" in factory and "Робото" in student_data['spec'] else 82
        if "Арсенал" in factory and "Лазер" in student_data['spec']: match_rate = 98
        
        st.metric(label="Совместимость цифрового следа с требованиями завода (Match Rate)", value=f"{match_rate}%")
        
        if st.button("Инициировать бесшовный b2b-мэтчинг кадров", use_container_width=True):
            with sqlite3.connect('prom_quality.db') as db_conn:
                db_cursor = db_conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db_cursor.execute(
                    "INSERT INTO student_shares (student_name, specialization, target_factory, match_rate, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (selected_student, student_data['spec'], factory, match_rate, now)
                )
                db_conn.commit()
            st.toast(f"Цифровой след успешно передан в HR-департамент компании {factory}!")

    st.write("---")
    st.subheader("📈 Аналитика: Прогноз дефицита инженеров в СПб (тыс. чел.)")
    years_list = list(range(2024, 2028))
    deficit_list = list([4.2, 5.8, 7.5, 9.1])
    chart_data = pd.DataFrame({
        "Год": years_list,
        "Дефицит кадров": deficit_list
    }).set_index("Год")
    st.line_chart(chart_data)

# ================= ВАРИАНТ 2: ШЕРИНГ-ЭКОНОМИКА =================
elif option == "Вариант 2: Шеринг-экономика & R&D (Арбитраж Авито)":
    st.header("🔬 Концепт: Шеринг свободных мощностей и оборудования НИИ")
    st.write("Коммерциализация научно-исследовательских лабораторий города с автоматическим расчетом стоимости контракта.")
    
    tab1, tab2 = st.tabs(["🛒 Маркетплейс R&D мощностей", "🤝 Финансовый арбитраж и Контроль SLA"])
    
    labs_pool = {
        "ЦНИИ КМ 'Прометей' (Лаборатория прочности)": {"price": 45000, "sla": 0.98},
        "ИТМО (Кафедра лазерных технологий)": {"price": 35000, "sla": 0.95},
        "Политех (Центр цифрового инжиниринга)": {"price": 50000, "sla": 0.99}
    }
    
    with tab1:
        st.subheader("Доступные слоты исследовательских институтов")
        selected_lab = st.selectbox("Выберите научно-техническую базу для проведения испытаний:", list(labs_pool.keys()))
        
        lab_info = labs_pool[selected_lab]
        st.info(f"**Стоимость аренды:** {lab_info['price']:,} руб/час | **Исторический рейтинг выполнения SLA:** {lab_info['sla']*100}%")
        
        st.write("---")
        st.subheader("📝 Конфигуратор и калькулятор b2b-сделки")
        with st.form("booking_form"):
            company = st.text_input("Название вашего предприятия:", placeholder="Например: ООО Северная Верфь")
            hours = st.number_input("Необходимое количество часов аренды / испытаний:", min_value=1, max_value=100, value=10)
            
            total_cost = int(hours * lab_info['price'])
            st.markdown(f"### Предварительная стоимость контракта: `{total_cost:,} руб.`")
            
            submitted = st.form_submit_button("Забронировать тайм-слот", use_container_width=True)
            if submitted:
                if not company.strip():
                    st.error("Ошибка: Введите название предприятия для формирования SLA-контракта.")
                else:
                    with sqlite3.connect('prom_quality.db') as db_conn:
                        db_cursor = db_conn.cursor()
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db_cursor.execute(
                            "INSERT INTO lab_bookings (company_name, lab_name, hours_requested, total_cost, timestamp) VALUES (?, ?, ?, ?, ?)",
                            (company, selected_lab, int(hours), total_cost, now)
                        )
                        db_conn.commit()
                    st.success(f"Контракт сформирован! Слот забронирован на {hours} ч. Итоговая сумма: {total_cost:,} руб.")
            
    with tab2:
        st.warning("⚠️ Дисциплина выполнения контрактов: НИИ 'Вектор' сорвал сроки выдачи заключения для завода 'Арсенал'. Платформа заблокировала b2b-выплату на расчетный счет НИИ до завершения экспертизы. Рейтинг SLA исполнителя снижен на 0.2 балла.")

# ================= ВАРИАНТ 3: СУПЕРАПП ОБРАЗОВАНИЯ =================
elif option == "Вариант 3: Финтех-Navigator образования (Экосистема Сбера)":
    st.header("🎒 Концепт: Финтех-трекер и субсидирование промышленного обучения")
    st.write("Сквозное планирование траектории инженера с расчетом финансовой модели и целевых b2b-грантов.")
    
    st.text_input("Укажите карьерную цель выпускника для построения финтех-модели:", "Инженер-конструктор авиационных двигателей")
    
    st.subheader("🗺 Карта сквозного бесшовного трека:")
    
    base_cost = 450000
    
    st.markdown("### 💳 Финансовая структура трека:")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric(label="Полная стоимость обучения в год", value=f"{base_cost:,} руб.")
    with col_f2:
        st.metric(label="Субсидия Правительства СПб (B2G)", value=f"- {int(base_cost*0.4):,} руб.", delta="40% покрытия")
    with col_f3:
        st.metric(label="Грант от завода (ОДК-Климов)", value=f"- {int(base_cost*0.6):,} руб.", delta="60% покрытия (Целевой контракт)")
        
    st.success("🔥 Итоговая стоимость для родителя/студента: 0 рублей! Обучение на 100% софинансируется экосистемой промышленности города.")

    st.write("---")
    st.subheader("📍 Географическая доступность инфраструктуры на карте СПб")
    map_data = pd.DataFrame({
        'lat': [59.9342, 59.9284, 59.9722],
        'lon': [30.3351, 30.3204, 30.3012]
    })
    st.map(map_data)
    st.button("Подписать целевой b2b-контракт электронной подписью", use_container_width=True)

# ================= МОНИТОРИНГ БД ДЛЯ АССОЦИАЦИИ =================
elif option == "📊 Панель Управления Ассоциации (Аудит БД)":
    st.header("📊 Сквозной b2b-мониторинг экосистемы")
    st.write("Панель Ассоциации промышленных производств для проверки транзакций, кадровых логов и исполнения SLA.")
    
    with sqlite3.connect('prom_quality.db') as db_conn:
        st.subheader("1. База сквозных кадровых мэтчингов (Яндекс-Логи)")
        try:
            df_students = pd.read_sql_query("SELECT id, student_name, specialization, target_factory, match_rate, timestamp FROM student_shares ORDER BY id DESC", db_conn)
            if not df_students.empty:
                st.dataframe(df_students, use_container_width=True)
            else:
                st.info("В базе данных экосистемы пока нет записей о передаче цифровых следов.")
        except Exception:
            st.info("Таблица логов студентов пуста или еще не инициализирована.")
            
        st.subheader("2. Реестр b2b-контрактов шеринга оборудования (Авито-Арбитраж)")
        try:
            df_bookings = pd.read_sql_query("SELECT id, company_name, lab_name, hours_requested, total_cost, timestamp FROM lab_bookings ORDER BY id DESC", db_conn)
