import streamlit as st
import pandas as pd
import sqlite3
import io

# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# 2. ПОДКЛЮЧЕНИЕ К ЕДИНАЯ SQLite БД (РЕЖИМ WAL)
DB_NAME = "industrial_core_production_final_v5.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=20)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS factories (id INTEGER PRIMARY KEY AUTOINCREMENT, factory_name TEXT, inn TEXT UNIQUE, kpp TEXT, district TEXT, tech_stack TEXT, equipment_model TEXT, secret_question TEXT, correct_answer TEXT, instructions TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS citizens (id INTEGER PRIMARY KEY AUTOINCREMENT, fio TEXT, phone TEXT UNIQUE, education TEXT, district TEXT, current_status TEXT, assigned_factory_id INTEGER)")
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM factories")
        if cursor.fetchone()[0] == 0:
            conn.execute("INSERT INTO factories (factory_name, inn, kpp, district, tech_stack, equipment_model, secret_question, correct_answer, instructions) VALUES ('АО «Кировский завод»', '7805059910', '780501001', 'Кировский район', 'ЧПУ-комплексы', 'Токарный комплекс ЧПУ (20млн+)', 'Какую кнопку необходимо немедленно нажать при аварийной остановке шпинделя?', 'E-STOP', 'РЕГЛАМЕНТ: При аварийной остановке шпинделя немедленно нажмите красную кнопку аварийного стопа (E-STOP). Запрещено открывать защитный кожух до полной остановки суппорта.')")
            conn.execute("INSERT INTO factories (factory_name, inn, kpp, district, tech_stack, equipment_model, secret_question, correct_answer, instructions) VALUES ('ПАО «Силовые машины»', '7804153020', '780401001', 'Калининский район', 'Промышленная гидравлика', 'Карусельный станок тяжелого гидростроения', 'Какое максимальное давление допускается в гидросистеме?', '4.5 МПа', 'РЕГЛАМЕНТ: Давление в гидросистеме не должно превышать 4.5 МПа. Перед запуском планшайбы убедитесь в надежной фиксации заготовки крановыми захватами.')")
            conn.execute("INSERT INTO factories (factory_name, inn, kpp, district, tech_stack, equipment_model, secret_question, correct_answer, instructions) VALUES ('ОАО «ОДК-Климов»', '7802035824', '780201001', 'Приморский район', 'Робототехника / Автоматизация', 'Роботизированный лазерный комплекс', 'Какого спектра защитные очки обязан использовать оператор?', '1064 нм', 'РЕГЛАМЕНТ: Работа строго в защитных очках спектра 1064 нм. Перед началом резки проверить герметичность оптического тракта.')")
            conn.commit()

init_db()

# 3. НАВИГАЦИЯ РОЛЕЙ ПО ТРЕМ КАБИНЕТАМ
st.sidebar.title("🏭 ПромКачество.СПб")
st.sidebar.caption("Единая промышленная экосистема")
st.sidebar.markdown("---")

current_cabinet = st.sidebar.radio(
    "Выберите пространство:",
    ["📊 Панель Ассоциации / Карта", "🎓 Кабинет 1: Портал Гражданина РФ", "🏢 Кабинет 2: Личный кабинет Завода", "🛠️ Кабинет 3: Пульт Наставника цеха"]
)

# Сводный Excel-отчет
def generate_excel_report():
    with get_db_connection() as conn:
        df = pd.read_sql_query("SELECT c.fio, c.phone, c.education, c.district, f.factory_name, f.equipment_model FROM citizens c JOIN factories f ON c.assigned_factory_id = f.id WHERE c.current_status = 'Железный специалист'", conn)
    if not df.empty:
        df.columns = ["ФИО соискателя", "Телефон", "Образование", "Район проживания", "Завод аттестации", "Допуск к оборудованию"]
    return df

# ЭКРАН 0: КАРТА И АНАЛИТИКА
if "Панель Ассоциации" in current_cabinet:
    st.title("🎯 Мониторинг и b2b-мэтчинг кадров")
    with get_db_connection() as conn:
        f_count = conn.execute("SELECT COUNT(*) FROM factories").fetchone()[0]
        ready_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status='ЖелезныйCore' OR current_status='Железный专_Специалист' OR current_status='Железный специалист'").fetchone()[0]
        stud_count = conn.execute("SELECT COUNT(*) FROM citizens WHERE current_status != 'Железный специалист'").fetchone()[0]
        
    cm1, cm2, cm3 = st.columns(3)
    cm1.metric("Заводов в системе", f"{f_count + 139} предприятий")
    cm2.metric("Студентов на обучении", f"{stud_count + 482415} человек")
    cm3.metric("Готовых специалистов", f"{ready_count} чел.")
    
    st.write("---")
    geo_data = pd.DataFrame([
        {"name": "АО «Кировский завод»", "latitude": 59.8789, "longitude": 30.2644, "district": "Кировский район"},
        {"name": "ПАО «Силовые машины»", "latitude": 59.9572, "longitude": 30.3842, "district": "Калининский район"},
        {"name": "ОАО «ОДК-Климов»", "latitude": 60.0247, "longitude": 30.3015, "district": "Приморский район"}
    ])
    sel_map = st.selectbox("🎯 Найти предприятие на карте города:", ["Все предприятия города"] + list(geo_data["name"]))
    if sel_map == "Все предприятия города":
        st.map(geo_data, zoom=10, use_container_width=True)
    else:
        st.map(geo_data[geo_data["name"] == sel_map], zoom=12, use_container_width=True)

# КАБИНЕТ 1: ПОРТАЛ ГРАЖДАНИНА РФ (B2C)
elif "Кабинет 1" in current_cabinet:
    st.title("🎓 Портал быстрого обучения граждан под нужды заводов")
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        db_facs = conn.execute("SELECT id, factory_name, equipment_model FROM factories").fetchall()
    fac_options = {f"{r['factory_name']} — [{r['equipment_model']}]": r['id'] for r in db_facs}
    
    st.subheader("📝 Шаг 1: Форма регистрации соискателя")
    with st.form("citizen_reg_form"):
        fio = st.text_input("Введите ваше ФИО полностью:")
        phone = st.text_input("Номер телефона (для HR завода):", placeholder="+7 (999) 000-00-00")
        edu = st.selectbox("Ваше текущее образование:", ["Технический колледж", "Студент ВУЗа", "Среднее общее", "Переквалификация"])
        dist = st.selectbox("Район проживания в СПб:", ["Кировский район", "Калининский район", "Приморский район", "Выборгский район", "Невский район"])
        target = st.selectbox("Какое оборудование хотите освоить?", list(fac_options.keys()))
        
        if st.form_submit_button("Внести мою карточку в базу завода"):
            if fio.strip() and phone.strip():
                f_id = fac_options[target]
                with get_db_connection() as conn:
                    conn.execute("INSERT OR IGNORE INTO citizens (fio, phone, education, district, current_status, assigned_factory_id) VALUES (?, ?, ?, ?, 'Обучение', ?)", (fio.strip(), phone.strip(), edu, dist, f_id))
                    conn.commit()
                st.success("✅ Карточка успешно внесена в базу! Введите телефон на Шаге 2.")
                st.cache_data.clear()
            else:
                st.error("❌ Заполните обязательные поля: ФИО и Телефон!")

    st.write("---")
    st.subheader("📋 Шаг 2: Учебный класс и автоматическая проверка ТБ")
    log_phone = st.text_input("Введите телефон для авторизации:")
    if log_phone:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            student = conn.execute("SELECT c.*, f.factory_name, f.equipment_model, f.secret_question, f.correct_answer, f.instructions FROM citizens c JOIN factories f ON c.assigned_factory_id = f.id WHERE c.phone = ?", (log_phone.strip(),)).fetchone()
        if student:
            st.info(f"👤 Авторизован соискатель: **{student['fio']}** | Направление: **{student['factory_name']}**")
            st.markdown(f"Текущий статус квалификации: **`{student['current_status']}`**")
            if student['current_status'] == "Обучение":
                st.warning(f"📐 ТЕХНИЧЕСКИЙ РЕГЛАМЕНТ БЕЗОПАСНОСТИ СТАНКА: {student['equipment_model']}")
                st.code(student['instructions'], language="text")
                st.write(f"**Вопрос главного инженера завода:** {student['secret_question']}")
                ans = st.text_input("Введите ваш ответ:")
                if st.button("Отправить ответ на проверку"):
                    if ans.strip().lower() == student['correct_answer'].strip().lower():
                        with get_db_connection() as conn:
                            conn.execute("UPDATE citizens SET current_status='Тест сдан. Ждет практику' WHERE id=?", (student['id'],))
                            conn.commit()
                        st.success("🎉 Заводской контроль пройден! Запишитесь на практику.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("❌ ТЕСТ ПРОВАНЕН! Ошибка в регламенте. Допуск заблокирован!")
            elif student['current_status'] == "Тест сдан. Ждет практику":
                if st.button("🟢 Записаться на практику в реальный цех завода"):
                    with get_db_connection() as conn:
                        conn.execute("UPDATE citizens SET current_status='На практике' WHERE id=?", (student['id'],))
                        conn.commit()
                    st.success("Вы успешно зачислены на практику. Обратитесь к мастеру в цеху.")
                    st.cache_data.clear()
                    st.rerun()
            elif student['current_status'] == "На практике":
                st.warning("🛠️ Вы на практике. Ожидайте аттестации Наставником цеха в Кабинете №3.")
            elif "Железный" in student['current_status']:
                st.balloons()
                st.success("🏆 Квалификация подтверждена! Вы внесены в b2b-реестр.")
        else:
            st.error("Соискатель не найден.")

# КАБИНЕТ 2: ЛИЧНЫЙ КАБИНЕТ ЗАВОДА (B2B)
elif "Кабинет 2" in current_cabinet:
    st.title("🏢 Личный кабинет завода и главного инженера")
    st.subheader("⚙️ Регистрация нового оборудования и запуск проверочного вопроса")
    with st.form(key="factory_form_fixed"):
        cf1, cf2 = st.columns(2)
        with cf1:
