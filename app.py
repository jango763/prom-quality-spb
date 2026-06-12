import streamlit as st
import pandas as pd

# Настройка страницы в строгом стиле B2B
st.set_page_config(page_title="Экосистема ПромКачество.СПб", layout="wide", page_icon="🏭")

# Сберовские CSS-инъекции: изумрудный зеленый, мягкие b2b-тени, неоновые метрики
st.markdown("""
    <style>
    /* Главный контейнер карточек */
    .sber-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 135, 90, 0.08);
        border-left: 6px solid #00875a;
        margin-bottom: 20px;
    }
    .sber-title {
        color: #00875a;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    /* Бейджи верификации */
    .badge-sber {
        background-color: #e6f4ea;
        color: #00875a;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
    /* Финтех-блок 0 рублей */
    .sber-metric-box {
        background: linear-gradient(135deg, #00875a 0%, #005e3e 100%);
        color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 135, 90, 0.2);
    }
    .sber-metric-val {
        font-size: 42px;
        font-weight: 800;
        color: #22c55e;
        margin: 10px 0;
        text-shadow: 0 2px 10px rgba(34, 197, 94, 0.3);
    }
    /* Витрина объявлений Авито/Сбер */
    .showcase-item {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .showcase-price {
        color: #00875a;
        font-weight: 700;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Экосистема «ПромКачество.СПб»")
st.caption("Цифровая b2b/b2c-платформа Ассоциации промышленных производств | Powered by Sber Design OS")

# Боковое меню выбора концепции
option = st.sidebar.radio(
    "Выберите вариант концепции для демонстрации:",
    ("Вариант 1: Кадровый хаб (Mэтчинг Яндекса)", 
     "Вариант 2: Шеринг-экономика & R&D (Арбитраж Авито)", 
     "Вариант 3: Финтех-Navigator образования (Экосистема Сбера)")
)

# ================= ВАРИАНТ 1: КАДРОВЫЙ ХАБ =================
if option == "Вариант 1: Кадровый хаб (Mэтчинг Яндекса)":
    st.header("🎯 Концепт: Умный b2b-мэтчинг и Цифровой след выпускника")
    st.write("Сквозной подбор молодых специалистов под нужды оборонно-промышленного и машиностроительного комплекса СПб.")
    
    students_db = {
        "Иванов Иван Игоревич (СПбПУ)": {
            "spec": "Робототехника и АСУ ТП", "qa": 4.9, 
            "skills": "Программирование ПЛК (Siemens/Codesys), КОМПАС-3D, SCADA-системы, C++",
            "vuz": "Санкт-Петербургский политехнический университет Петра Великого"
        },
        "Петров Пётр Георгиевич (НИУ ИТМО)": {
            "spec": "Оптические и Квантовые технологии", "qa": 4.8, 
            "skills": "Лазерная резка/напыление, Программирование CNC-станков, Оптическая физика, Python",
            "vuz": "Национальный исследовательский университет ИТМО"
        },
        "Сидоров Константин Михайлович (СПбГЭТУ 'ЛЭТИ')": {
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
        
        # Сберовская b2b-карточка студента
        st.markdown(f"""
            <div class="sber-card">
                <div class="badge-sber">✓ QA Verified Profile</div>
                <div class="sber-title">{selected_student.split(' (')[0]}</div>
                <p><b>Вуз:</b> {student_data['vuz']}</p>
                <p><b>Направление:</b> {student_data['spec']}</p>
                <p><b>Рейтинг компетенций Ассоциации:</b> ⭐️ {student_data['qa']} / 5.0</p>
            </div>
        """, unsafe_allow_html=True)
        st.success(f"**Подтвержденные hard-skills:** {student_data['skills']}")
    
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
            st.toast(f"Цифровой след успешно направлен в HR-департамент компании {factory}!")

# ================= ВАРИАНТ 2: ШЕРИНГ-ЭКОНОМИКА (R&D) =================
elif option == "Вариант 2: Шеринг-экономика & R&D (Арбитраж Авито)":
    st.header("🔬 Концепт: Шеринг свободных мощностей и оборудования НИИ")
    st.write("Промышленный маркетплейс оборудования с автоматическим расчетом SLA и стоимости контракта.")
    
    tab1, tab2 = st.tabs(["🛒 Маркетплейс R&D мощностей", "🤝 Финансовый арбитраж и Контроль SLA"])
    
    labs_pool = {
        "ЦНИИ КМ 'Прометей' (Лаборатория материаловедения)": {"price": 45000, "sla": 98, "desc": "Испытания металлов и композитов на прочность, усталость и радиационную стойкость."},
        "Университет ИТМО (Кафедра лазерных технологий)": {"price": 35000, "sla": 95, "desc": "Высокоточная лазерная резка, 3D-напыление металлических покрытий и прецизионная оптика."},
        "СПбПУ (Центр компьютерного инжиниринга)": {"price": 50000, "sla": 99, "desc": "Разработка цифровых двойников изделий, виртуальные краш-тесты и топологическая оптимизация."},
        "АО 'ГОИ им. С.И. Вавилова' (Оптическая лаборатория)": {"price": 42000, "sla": 94, "desc": "Тестирование оптико-электронных систем, напыление просветляющих слоев и спектрометрия."}
    }
    
    with tab1:
        st.subheader("Доступные слоты научно-технических центров")
        selected_lab = st.selectbox("Выберите научно-техническую базу для проведения испытаний:", list(labs_pool.keys()))
        lab_info = labs_pool[selected_lab]
        
        # Сберовская b2b-карточка лаборатории
        st.markdown(f"""
            <div class="sber-card">
                <div class="sber-title">{selected_lab}</div>
                <p><b>Спецификация:</b> {lab_info['desc']}</p>
                <p class="showcase-price">Базовый тариф: {lab_info['price']:,} руб/час</p>
                <p><b>Надежность по SLA:</b> {lab_info['sla']}% своевременного выполнения</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📝 Расчет b2b-сделки")
        company = st.text_input("Название вашего предприятия:", placeholder="Например: ПАО СЗ 'Северная верфь'")
        hours = st.number_input("Количество испытательных часов:", min_value=1, max_value=150, value=10)
        
        total_cost = int(hours * lab_info['price'])
        st.markdown(f"### Итоговая стоимость SLA-контракта: <span style='color:#00875a;'>{total_cost:,} руб.</span>", unsafe_allow_html=True)
        
        if st.button("Забронировать тайм-слот оборудования", use_container_width=True):
            if not company.strip():
                st.error("Ошибка: Введите название предприятия для автоматической генерации контракта.")
            else:
                st.success(f"Контракт сформирован! Слот в {selected_lab} забронирован на {hours} ч. Сумма контракта: {total_cost:,} руб.")
            
    with tab2:
        st.warning("⚠️ Дисциплина выполнения контрактов: НИИ 'Вектор' сорвал регламентные сроки выдачи отчетов по ТЗ для АО 'Завод Арсенал'. Платформа автоматически заблокировала b2b-транзакцию на расчетный счет НИИ до завершения технического аудита. Текущий рейтинг SLA исполнителя снижен на 0.2 балла.")

# ================= ВАРИАНТ 3: СУПЕРАПП ОБРАЗОВАНИЯ (СБЕР) =================
elif option == "Вариант 3: Финтех-Navigator образования (Экосистема Сбера)":
    st.header("🎒 Концепт: Финтех-трекер и субсидирование промышленного обучения")
    st.write("Сквозное планирование траектории инженера с расчетом финансовой модели и целевых b2b-грантов.")
    
    st.text_input("Укажите карьерную цель выпускника для построения финтех-модели:", "Инженер-конструктор авиационных двигателей")
    
    st.subheader("🗺 Карта сквозного бесшовного трека:")
    
    base_cost = 450000
    st.markdown("### 💳 Финансовая структура трека:")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric(label="Полная стоимость обучения инженера в год", value=f"{base_cost:,} руб.")
    with col_f2:
        st.metric(label="Субсидия Правительства СПб (B2G)", value=f"- {int(base_cost*0.4):,} руб.", delta="40% покрытия")
    with col_f3:
        st.metric(label="Целевой грант завода (ОДК-Климов)", value=f"- {int(base_cost*0.6):,} руб.", delta="60% покрытия")
        
    # Премиальный Сберовский блок метрики
    st.markdown("""
        <div class="sber-metric-box">
            <div style="font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Итоговая стоимость для родителя / студента:</div>
            <div class="sber-metric-val">0 РУБЛЕЙ</div>
