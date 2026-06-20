import streamlit as st
import pandas as pd

# Настройка страницы в стиле B2B
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# --- Инициализация состояния сессии ---
if "matches_history" not in st.session_state: st.session_state.matches_history = []
if "bookings_history" not in st.session_state: st.session_state.bookings_history = []
if "parent_leads" not in st.session_state: st.session_state.parent_leads = []

# Инициализация переменных для нового Варианта 4 (Финтех и ДПО)
if "sm_factory_balance" not in st.session_state: st.session_state.sm_factory_balance = 1500.00
if "sm_is_premium" not in st.session_state: st.session_state.sm_is_premium = False
if "sm_courses" not in st.session_state:
    st.session_state.sm_courses = [
        {"title": "Работа на токарных станках ЧПУ серии ИТ-42", "factory": "АО 'Кировский завод'"},
        {"title": "Стандартизация промышленной гидравлики", "factory": "АО 'Силовые машины'"}
    ]
if "sm_leads" not in st.session_state:
    st.session_state.sm_leads = [
        {"name": "Иванов Иван Игоревич", "phone": "+7 (999) 111-22-33", "course": "Работа на токарных станках ЧПУ серии ИТ-42", "status": "Заморожен"},
        {"name": "Петров Петр Георгиевич", "phone": "+7 (999) 444-55-66", "course": "Стандартизация промышленной гидравлики", "status": "Заморожен"}
    ]

st.title("Экосистема «ПромКачество.СПб»")

# Боковое меню
option = st.sidebar.radio(
    "Выберите вариант концепции:",
    ("Вариант 1: Кадровый хаб", "Вариант 2: Шеринг-экономика", "Вариант 3: Финтех-Navigator", "🔥 Вариант 4: Экосистема ДПО (Проект С.М.)", "📊 Панель Ассоциации")
)

# --- БЛОКИ КОНЦЕПЦИЙ ---
if option == "Вариант 1: Кадровый хаб":
    st.header("🎯 Умный b2b-мэтчинг")
    # ... (код мэтчинга)
elif option == "Вариант 2: Шеринг-экономика":
    st.header("🔬 Маркетплейс R&D мощностей")
    # ... (код шеринга)
elif option == "Вариант 3: Финтех-Navigator":
    st.header("🎒 Конфигуратор обучения")
    # ... (код навигатора)
elif option == "🔥 Вариант 4: Экосистема ДПО (Проект С.М.)":
    st.header("🏭 Промышленное ДПО и Лидогенерация")
    sm_tab1, sm_tab2, sm_tab3 = st.tabs(["🏢 Завод", "🎓 Ученик", "💥 Трафик"])
    
    with sm_tab1:
        st.metric(label="Баланс (CPA)", value=f"{st.session_state.sm_factory_balance:,.2f} руб.")
        if not st.session_state.sm_is_premium:
            if st.button("Активировать Безлимит"):
                st.session_state.sm_is_premium = True
                st.rerun()
        # Лиды
        for idx, lead in enumerate(st.session_state.sm_leads):
            with st.container(border=True):
                c_name, c_act = st.columns([3, 1])
                is_unlocked = st.session_state.sm_is_premium or lead["status"] == "Разблокирован"
                c_name.write(f"👤 {lead['name'] if is_unlocked else 'Лид скрыт'}")
                if not is_unlocked:
                    if c_act.button(f"Выкупить", key=f"sm_buy_{idx}"):
                        if st.session_state.sm_factory_balance >= 500:
                            st.session_state.sm_factory_balance -= 500
                            st.session_state.sm_leads[idx]["status"] = "Разблокирован"
                            st.rerun()
                else: c_act.write(f"📞 {lead['phone']}")
                    
    with sm_tab2:
        for c_idx, course in enumerate(st.session_state.sm_courses):
            with st.container(border=True):
                st.write(f"### {course['title']}")
                if st.button("🚀 Пройти курс", key=f"stud_btn_{c_idx}"):
                    st.session_state.sm_leads.append({"name": "Новый Выпускник", "course": course['title'], "status": "Заморожен"})
                    st.rerun()
                    
    with sm_tab3:
        st.error("🔥 ШОК! Скрытые доходы через ДПО АПП СПб!")
        if st.button("ЗАРЕГИСТРИРОВАТЬСЯ", use_container_width=True): st.balloons()

elif option == "📊 Панель Ассоциации":
    st.header("📊 Мониторинг экосистемы")
    # ... (код панели)
