import streamlit as st
import pandas as pd

# Настройка страницы в строгом стиле B2B
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# Инициализация оперативной памяти сессии (Замена тяжелой БД)
if "matches_history" not in st.session_state:
    st.session_state.matches_history = []
if "bookings_history" not in st.session_state:
    st.session_state.bookings_history = []

st.title("Экосистема «ПромКачество.СПб»")
st.caption("Флагманский b2b/b2c-прототип платформы для Ассоциации промышленных производств")

# Боковое меню выбора концепции
option = st.sidebar.radio(
    "Выберите вариант концепции для демонстрации:",
    ("Вариант 1: Кадровый хаб (Mэтчинг Яндекса)", 
     "Вариант 2: Шеринг-экономика & R&D (Арбитраж Авито)", 
     "Вариант 3: Финтех-Navigator образования (Экосистема Сбера)",
     "📊 Панель Ассоциации (Оперативный аудит)")
)

# ================= ВАРИАНТ 1: КАДРОВЫЙ ХАБ =================
if option == "Вариант 1: Кадровый хаб (Mэтчинг Яндекса)":
    st.header("🎯 Концепт: Умный b2b-мэтчинг и Цифровой след выпускника")
    st.write("Интеллектуальный подбор молодых специалистов под нужды оборонно-промышленного комплекса СПб.")
    
    students_db = {
        "Иванов Иван Игоревич (СПбПУ)": {
            "spec": "Робототехника и АСУ ТП", "qa": 4.9, 
            "skills": "Программирование ПЛК (Siemens/Codesys), КОМПАС-3D, SCADA-системы, C++",
            "vuz": "Санкт-Петербургский политехнический университет Петра Великого"
        },
        "Petrov Petr Georgievich (ITMO)": {
            "spec": "Оптические и Квантовые технологии", "qa": 4.8, 
            "skills": "Лазерная резка/напыление, Программирование CNC-станков, Оптическая физика, Python",
            "vuz": "Национальный исследовательский университет ИТМО"
        },
        "Сидоров Константин Михайлович (ЛЭТИ)": {
            "spec": "Проектирование микроэлектроники", "qa": 4.6, 
            "skills": "Проектирование печатных плат (Altium Designer), VHDL/Verilog, Работа в чистых помещениях",
            "vuz": "СПбГЭТУ 'ЛЭТИ'"
        }
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👤 Цифровая база соискателей вузов:")
        selected_student = st.selectbox("Выберите верифицированного выпускника:", list(students_db.keys()))
        student_data = students_db[selected_student]
        
        st.info(f"Выпускник: {selected_student}\n\nВуз: {student_data['vuz']}\n\nНаправление: {student_data['spec']}\n\nРейтинг QA: {student_data['qa']} / 5.0")
        st.success(f"Подтвержденные hard-skills: {student_data['skills']}")
    
    with col2:
        st.subheader("🏭 Отраслевые b2b-заказчики:")
        factory = st.selectbox(
            "Выберите промышленное предприятие СПб:", 
            ["АО 'Кировский завод'", "АО 'Силовые машины'", "АО 'ОДК-Климов'", "АО 'Адмиралтейские верфи'", "ПАО 'СЗ 'Северная верфь'", "АО 'ОАО Завод Арсенал'"]
        )
        
        match_rate = 85
        if "Кировский" in factory and "Робото" in student_data['spec']: match_rate = 96
        elif "Силовые машины" in factory and "Робото" in student_data['spec']: match_rate = 94
        elif "ОДК-Климов" in factory and "Оптиче" in student_data['spec']: match_rate = 92
        elif "Арсенал" in factory and "Оптиче" in student_data['spec']: match_rate = 98
        
        st.metric(label="Совместимость цифрового следа со стандартами предприятия (Match Rate)", value=f"{match_rate}%")
        
        if st.button("Инициировать бесшовный мэтчинг кадров", use_container_width=True):
            st.session_state.matches_history.append({
                "Соискатель": selected_student,
                "Направление": student_data['spec'],
                "Предприятие": factory,
                "Совместимость": f"{match_rate}%"
            })
            st.toast(f"Цифровой след успешно передан в HR-департамент компании {factory}!")

# ================= ВАРИАНТ 2: ШЕРИНГ-ЭКОНОМИКА =================
elif option == "Вариант 2: Шеринг-экономика & R&D (Арбитраж Авито)":
    st.header("🔬 Концепт: Шеринг свободных мощностей и оборудования НИИ")
    st.write("Промышленный маркетплейс оборудования с автоматическим расчетом SLA и стоимости контракта.")
    
    tab1, tab2 = st.tabs(["🛒 Маркетплейс R&D мощностей", "🤝 Финансовый арбитраж и Контроль SLA"])
    
    labs_pool = {
        "ЦНИИ КМ 'Прометей' (Лаборатория материаловедения)": {"price": 45000, "sla": 98, "desc": "Испытания металлов и композитов на прочность, усталость и радиационную стойкость."},
        "Университет ИТМО (Кафедра лазерных технологий)": {"price": 35000, "sla": 95, "desc": "Высокоточная лазерная резка, 3D-напыление металлических покрытий и прецизионная оптика."},
        "СПбПУ (Центр компьютерного инжиниринга)": {"price": 50000, "sla": 99, "desc": "Разработка цифровых двойников изделий, виртуальные краш-тесты и топологическая оптимизация."}
    }
    
    with tab1:
        st.subheader("Доступные слоты научно-технических центров")
        selected_lab = st.selectbox("Выберите научно-техническую базу для проведения испытаний:", list(labs_pool.keys()))
        lab_info = labs_pool[selected_lab]
        
        st.info(f"Лаборатория: {selected_lab}\n\nСпецификация: {lab_info['desc']}\n\nБазовый тариф: {lab_info['price']:,} руб/час\n\nНадежность по SLA: {lab_info['sla']}%")
        
        st.write("---")
        st.subheader("📝 Расчет b2b-сделки")
        company = st.text_input("Название вашего предприятия:", placeholder="Например: ПАО СЗ 'Северная верфь'")
        hours = st.number_input("Количество испытательных часов:", min_value=1, max_value=150, value=10)
        
        total_cost = int(hours * lab_info['price'])
        st.write(f"### Итоговая стоимость SLA-контракта: {total_cost:,} руб.")
        
        if st.button("Забронировать тайм-слот оборудования", use_container_width=True):
            if not company.strip():
                st.error("Ошибка: Введите название предприятия для формирования SLA-контракта.")
            else:
                st.session_state.bookings_history.append({
                    "Предприятие-заказчик": company,
                    "Научный центр": selected_lab,
                    "Испытательные часы": hours,
                    "Итоговый бюджет": f"{total_cost:,} руб."
                })
                st.success(f"Контракт сформирован! Слот в {selected_lab} забронирован на {hours} ч. Сумма контракта: {total_cost:,} руб.")
            
    with tab2:
        st.warning("⚠️ Дисциплина выполнения контрактов: НИИ 'Вектор' сорвал регламентные сроки выдачи отчетов по ТЗ для АО 'Завод Арсенал'. Платформа автоматически заблокировала b2b-транзакцию на расчетный счет НИИ до завершения технического аудита.")

# ================= ВАРИАНТ 3: СУПЕРАПП ОБРАЗОВАНИЯ =================
elif option == "Вариант 3: Финтех-Navigator образования (Экосистема Сбера)":
    st.header("🎒 Концепт: Пошаговый конфигуратор промышленного обучения ребенка")
    st.write("Сконструируйте бесшовную траекторию обучения, проложите маршрут практики и подайте заявку на целевой грант.")
    
    # Инициализация списка лидов родителей в сессии, если его еще нет
    if "parent_leads" not in st.session_state:
        st.session_state.parent_leads = []

    # Справочники вузов и заводов с координатами
    vuz_pool = {
        "СПбПУ (Политех)": {"cost": 420000, "lat": 59.9994, "lon": 30.3744, "spec": "АСУ ТП и Системный инжиниринг"},
        "НИУ ИТМО": {"cost": 460000, "lat": 59.9572, "lon": 30.3081, "spec": "Квантовые и Лазерные технологии"},
        "СПбГЭТУ 'ЛЭТИ'": {"cost": 380000, "lat": 59.9722, "lon": 30.3211, "spec": "Микроэлектроника и Нанотехнологии"},
        "ГУАП": {"cost": 350000, "lat": 59.9284, "lon": 30.3204, "spec": "Авиастроение и Проектирование БПЛА"}
    }
    
    factory_pool = {
        "АО 'Кировский завод'": {"lat": 59.8824, "lon": 30.2521, "desc": "Тяжелое машиностроение"},
        "АО 'ОДК-Климов'": {"lat": 59.8315, "lon": 30.3421, "desc": "Авиационное двигателестроение"},
        "АО 'Завод Арсенал'": {"lat": 59.9711, "lon": 30.3722, "desc": "Космическое и приборостроение"},
        "АО 'Силовые машины'": {"lat": 59.8967, "lon": 30.3544, "desc": "Энергетическое машиностроение"}
    }
    
    # Конфигуратор для Родителя
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        st.subheader("1. Выберите Высшее учебное заведение:")
        chosen_vuz = st.selectbox("Доступные технические вузы СПб:", list(vuz_pool.keys()))
    with col_in2:
        st.subheader("2. Выберите индустриального партнера (Завод):")
        chosen_factory = st.selectbox("Предприятия, выдающие целевые b2b-гранты:", list(factory_pool.keys()))
        
    st.write("---")
    
    # Динамический финтех-расчет на основе выбора
    base_cost = vuz_pool[chosen_vuz]["cost"]
    gov_subsidy = int(base_cost * 0.40) 
    factory_grant = int(base_cost * 0.60) 
    parent_pays = base_cost - gov_subsidy - factory_grant
    
    st.subheader(f"💳 Анализ финансовой структуры трека для направления '{vuz_pool[chosen_vuz]['spec']}':")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric(label=f"Стоимость обучения в {chosen_vuz} (в год)", value=f"{base_cost:,} руб.")
    with col_f2:
        st.metric(label="Субсидия Правительства СПб (B2G)", value=f"- {gov_subsidy:,} руб.", delta="40% покрытия")
    with col_f3:
        st.metric(label=f"Грант от {chosen_factory}", value=f"- {factory_grant:,} руб.", delta="60% покрытия")
        
    st.info(f"🔥 ИТОГО к оплате родителю: {parent_pays} РУБЛЕЙ! Обучение полностью софинансируется городом и заводом.")

    # Логистика трека на карте Санкт-Петербурга с прорисовкой линии маршрута
    st.subheader("📍 Интерактивный b2b-маршрут практики на карте")
    st.write(f"Маршрут связывает локацию обучения (**{chosen_vuz}**) и производственную площадку (**{chosen_factory}**).")
    
    map_df = pd.DataFrame({
        'lat': [vuz_pool[chosen_vuz]["lat"], factory_pool[chosen_factory]["lat"]],
        'lon': [vuz_pool[chosen_vuz]["lon"], factory_pool[chosen_factory]["lon"]]
    })
    st.map(map_df)

    # ИНТЕРАКТИВНАЯ ФОРМА ЗАПИСИ ДЛЯ РОДИТЕЛЕЙ (РЕШЕНИЕ ПРОБЛЕМЫ "РЕКЛАМКИ")
    st.write("---")
    st.subheader("📝 Направление электронной заявки на целевое обучение")
    st.write("Заполните форму ниже, чтобы зафиксировать цифровой след вашего ребенка в реестре Ассоциации.")
    
    with st.form("parent_enrollment_form"):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            parent_fio = st.text_input("ФИО Родителя / Законного представителя:", placeholder="Например: Петров Георгий Николаевич")
            parent_phone = st.text_input("Контактный телефон для связи:", placeholder="+7 (999) 000-00-00")
        with col_form2:
            child_fio = st.text_input("ФИО Студента / Абитуриента:", placeholder="Например: Петров Александр Георгиевич")
            child_class = st.selectbox("Текущий статус обучения ребенка:", ["Выпускной класс школы (11 класс)", "Студент 1-2 курса колледжа", "Абитуриент вуза"])
            
        submit_lead = st.form_submit_button("Подать заявку и подписать согласие на целевой трек", use_container_width=True)
        
        if submit_lead:
            if not parent_fio.strip() or not parent_phone.strip() or not child_fio.strip():
                st.error("Ошибка: Пожалуйста, заполните все обязательные поля формы для отправки заявки.")
            else:
                # Физически записываем лид в память сессии
                st.session_state.parent_leads.append({
                    "Дата/Время": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Родитель": parent_fio,
                    "Телефон": parent_phone,
                    "Ребенок": child_fio,
                    "Статус": child_class,
                    "Выбранный ВУЗ": chosen_vuz,
                    "Выбранный Завод": chosen_factory
                })
                st.success(f"Уважаемый {parent_fio}! Заявка на целевой трек в {chosen_vuz} под b2b-заказ {chosen_factory} успешно сформирована. Цифровой след сохранен.")

# ================= ОПЕРАТИВНАЯ ПАНЕЛЬ СЕССИИ ДЛЯ АССОЦИАЦИИ =================
elif option == "📊 Панель Ассоциации (Оперативный аудит)":
    st.header("📊 Оперативный b2b/b2c-мониторинг экосистемы")
    st.write("Сквозной аудит транзакций, кадровых логов и входящих заявок от пользователей в реальном времени.")
    
    st.subheader("1. Активные кадровые мэтчинги студентов (Вариант 1 — Яндекс)")
    if st.session_state.matches_history:
        st.dataframe(pd.DataFrame(st.session_state.matches_history), use_container_width=True)
    else:
        st.info("В текущей сессии еще не было кликов по студентам.")
        
    st.subheader("2. Сформированные b2b-контракты шеринга оборудования (Вариант 2 — Авито)")
    if st.session_state.bookings_history:
        st.dataframe(pd.DataFrame(st.session_state.bookings_history), use_container_width=True)
    else:
        st.info("В текущей сессии еще не оформлялись b2b-контракты лабораторий.")
        
    # НОВАЯ ТАБЛИЦА ЛИДОВ ОТ РОДИТЕЛЕЙ (СБЕР)
    st.subheader("3. Заявки от родителей на софинансирование обучения (Вариант 3 — Сбер Лиды)")
    if "parent_leads" in st.session_state and st.session_state.parent_leads:
        df_leads = pd.DataFrame(st.session_state.parent_leads)
        st.dataframe(df_leads, use_container_width=True)
        
        csv_leads = df_leads.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Скачать базу b2c-заявок родителей в CSV", data=csv_leads, file_name="parent_leads.csv", mime="text/csv", use_container_width=True)
    else:
        st.info("В текущей сессии заявок от родителей еще не поступало. Заполните форму записи в Варианте 3!")
