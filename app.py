import streamlit as st
import pandas as pd
import random
import numpy as np

# ==============================================================================
# 1. КОНФИГУРАЦИЯ СТРАНИЦЫ И СТИЛИ (Добавлена темная индустриальная тема)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Экосистема", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #4A5568; }
        div[data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; color: #0284C7; }
        .highlight-box { padding: 20px; border-radius: 12px; background-color: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 15px; }
        
        /* Стиль для главного индустриального баннера */
        .hero-banner {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            padding: 40px;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 30px;
            border-left: 8px solid #0284C7;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .hero-title { font-size: 38px; font-weight: 800; color: #FFFFFF; margin-bottom: 5px; }
        .hero-subtitle { font-size: 18px; color: #94A3B8; font-weight: 400; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (State)
# ==============================================================================
if "app_platform" not in st.session_state:
    st.session_state["app_platform"] = {
        "balance": 25000.00,
        "is_premium": False,
        "courses": [
            {"id": "c1", "title": "Отказоустойчивость гидравлических систем", "factory": "АО 'Силовые машины'", "clicks": 1420, "leads": 84, "color": "🔵"},
            {"id": "c2", "title": "Программирование ЧПУ циклов серии ИТ-42", "factory": "АО 'Кировский завод'", "clicks": 2850, "leads": 196, "color": "⚙️"},
            {"id": "c3", "title": "Метрология и лазерный контроль геометрии", "factory": "Обуховский завод", "clicks": 930, "leads": 41, "color": "🔬"}
        ],
        "leads": [
            {"id": "l1", "name": "Александров К.М. (Военмех)", "phone": "+7 (921) 345-67-89", "course": "Программирование ЧПУ циклов серии ИТ-42", "status": "Заморожен", "rating": "⭐ 4.9"},
            {"id": "l2", "name": "Дмитриев А.В. (СПбПУ)", "phone": "+7 (911) 987-65-43", "course": "Отказоустойчивость гидравлических систем", "status": "Заморожен", "rating": "⭐ 4.7"}
        ]
    }

if "student_form_cache" not in st.session_state:
    st.session_state["student_form_cache"] = {"active_course_id": None, "test_passed": False}

db = st.session_state["app_platform"]
cache = st.session_state["student_form_cache"]

# ==============================================================================
# 3. САЙДБАР: НАВИГАЦИЯ И ДОСТУП
# ==============================================================================
with st.sidebar:
    st.title("👨‍💼 Профиль")
    user_role = st.selectbox(
        "Выбор рабочего пространства:",
        ["🏢 Предприятие / Завод (B2B)", "🎓 Гражданин / Ученик (B2C)", "💥 Маркетолог (Тизерный хаб)"]
    )
    st.write("---")
    st.caption("🔒 Защищенный цифровой периметр АПП Санкт-Петербурга")

# ==============================================================================
# 4. ПАРАДНАЯ ШАПКА ПЛАТФОРМЫ (Убираем белый пустой экран)
# ==============================================================================
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Цифровая экосистема «ПромКачество.СПб»</div>
        <div class="hero-subtitle">Федеральный каркас опережающего ДПО и автоматической лидогенерации АПП СПБ</div>
    </div>
""", unsafe_allow_html=True)

# ЖИВЫЕ ГЛОБАЛЬНЫЕ KPI ПЛАТФОРМЫ (Показывают масштаб Спонсору)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Подключено заводов СПб", value="142 предприятия", delta="+4 за неделю")
kpi2.metric(label="Граждан на обучении", value="482,900 чел.", delta="Охват регионов РФ")
kpi3.metric(label="Сгенерировано лидов", value="18,410 заявок", delta="Конверсия 91%")
kpi4.metric(label="Общий оборот финтех-эквайринга", value="4.2 млн ₽", delta="CPA модель")

st.write("---")

# ==============================================================================
# 🏢 ИНТЕРФЕЙС РОЛИ: ЗАВОД
# ==============================================================================
if user_role == "🏢 Предприятие / Завод (B2B)":
    st.subheader("📊 Мониторинг b2b-бюджета и цифрового кадрового следа")
    
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Ваш финтех-баланс (CPA)", value=f"{db['balance']:,.2f} ₽")
    tariff_txt = "БЕЗЛИМИТ" if db["is_premium"] else "CPA (500₽/лид)"
    c2.metric(label="Текущий B2B-тариф", value=tariff_txt)
    c3.metric(label="Ваши целевые лиды", value=len(db["leads"]))
    
    if not db["is_premium"]:
        if st.button("🔌 Переключить всю экосистему на Безлимитный Годовой Пакет", use_container_width=True, type="primary"):
            db["is_premium"] = True
            st.success("Экосистема переведена в режим безлимитного трафика!")
            st.rerun()

    st.write("---")
    st.subheader("📈 Динамика вовлечения кадров на ваши курсы")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Кликбейт', 'ДПО', 'Лиды']).cumsum()
    st.line_chart(chart_data)

    st.write("---")
    st.subheader("🎯 Поступившие горячие лиды (Кандидаты)")
    
    if not db["leads"]:
        st.info("💡 На данный момент поступивших лидов нет. Сгенерируйте их, пройдя курс во вкладке 'Гражданин / Ученик'.")
    else:
        for idx, lead in enumerate(db["leads"]):
            with st.container(border=True):
                st.markdown(f"**Курс:** {lead['course']} | **Рейтинг:** {lead['rating']}")
                c_info, c_act = st.columns(2)
                is_open = db["is_premium"] or lead["status"] == "Разблокирован"
                c_info.write(f"**ФИО соискателя:** {lead['name'] if is_open else '🔒 Скрыто системой CPA'}")
                
                if not is_open:
                    has_money = db["balance"] >= 500
                    btn_name = "💳 Открыть контакт (500 ₽)" if has_money else "❌ Пополните счет"
                    if c_act.button(btn_name, key=f"factory_buy_{lead['id']}_{idx}", use_container_width=True, disabled=not has_money):
                        db["balance"] -= 500
                        db["leads"][idx]["status"] = "Разблокирован"
                        st.rerun()
                else:
                    c_act.success(f"📞 {lead['phone']}")

# ==============================================================================
# 🎓 ИНТЕРФЕЙС РОЛИ: УЧЕНИК
# ==============================================================================
elif user_role == "🎓 Гражданин / Ученик (B2C)":
    st.subheader("🎓 Интерактивная академия профессиональной подготовки")
    
    st.write("---")
    st.subheader("📍 Карта распределения промышленных мощностей")
    map_data = pd.DataFrame({'lat': [59.9004, 59.8821, 59.8341], 'lon': [30.4322, 30.2743, 30.4912]})
    st.map(map_data, size=40)

    st.write("---")
    st.subheader("📋 Доступные программы опережающей подготовки:")
    
    if not db["courses"]:
        st.warning("⚠️ Каталог курсов пуст.")
    else:
        for idx, course in enumerate(db["courses"]):
            with st.container(border=True):
                col_icon, col_txt, col_btn = st.columns([1, 4, 2])
                col_icon.write(f"# {course['color']}")
                col_txt.write(f"### {course['title']}")
                col_txt.write(f"🏭 Индустриальный автор: **{course['factory']}**")
                
                if col_btn.button("🚀 Начать бесплатное обучение", key=f"student_start_{course['id']}_{idx}", use_container_width=True):
                    cache["active_course_id"] = course['id']
                    cache["test_passed"] = True
                    
                    random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
                    db["leads"].append({
                        "id": f"gen_l_{random.randint(1000, 9999)}",
                        "name": f"Выпускник академии №{random.randint(100, 999)}",
                        "phone": f"+7 (9xx) {random_digits[:3]}-{random_digits[3:5]}-{random_digits[5:]}",
                        "course": course['title'],
                        "status": "Заморожен",
                        "rating": f"⭐ {random.uniform(4.5, 5.0):.1f}"
                    })
                    st.balloons()
                    st.rerun()
                
                if cache["active_course_id"] == course['id'] and cache["test_passed"]:
                    st.success("🎯 Доступ к симулятору открыт! Ваше цифровое резюме направлено в HR-отдел завода.")
                    st.markdown("""
                    <div style="padding:15px; background-color:#ECFDF5; border-left: 5px solid #10B981; border-radius:4px;">
                        <b>Программа запущенного модуля:</b><br>
                        1. Изучение технического регламента оборудования завода.<br>
                        2. Автоматическая отправка верифицированного резюме в HR-отдел после теста.
                    </div>
                    """, unsafe_allow_html=True)

# ==============================================================================
# 💥 ИНТЕРФЕЙС РОЛИ: МАРКЕТОЛОГ
# ==============================================================================
elif user_role == "💥 Маркетолог платформы (Трафик)":
    st.subheader("💥 Панель вирусного вовлечения b2c-аудитории")
    
    if not db["courses"]:
        st.info("📊 Сводная таблица аналитики пуста.")
    else:
        marketing_df = pd.DataFrame(db["courses"])
        st.dataframe(
            marketing_df[['title', 'factory', 'clicks', 'leads']],
