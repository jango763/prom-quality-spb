import streamlit as st
import pandas as pd

# 1. Жесткое правило: Конфигурация страницы на самой первой строчке кода
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# ==============================================================================
# 2. УНИЧТОЖЕНИЕ МАГИЧЕСКИХ СТРОК (Константы меню)
# ==============================================================================
class MenuOptions:
    HUB = "Вариант 1: Кадровый хаб (Мэтчинг)"
    SHARING = "Вариант 2: Шеринг-экономика & R&D"
    NAVIGATOR = "Вариант 3: Финтех-Navigator образования"
    PROJECT_SM = "🔥 Вариант 4: Экосистема ДПО (Проект С.М.)"
    AUDIT = "📊 Панель Ассоциации (Аудит)"

# ==============================================================================
# 3. СГРУППИРОВАННАЯ ИНИЦИАЛИЗАЦИЯ STATE (Наводим порядок в памяти)
# ==============================================================================
if "matches_history" not in st.session_state: st.session_state.matches_history = []
if "bookings_history" not in st.session_state: st.session_state.bookings_history = []
if "parent_leads" not in st.session_state: st.session_state.parent_leads = []

# Группируем все финтех-переменные проекта С.М. в один изолированный словарь
if "sm_project" not in st.session_state:
    st.session_state["sm_project"] = {
        "balance": 1500.00,
        "is_premium": False,
        "courses": [
            {"title": "Работа на токарных станках ЧПУ серии ИТ-42", "factory": "АО 'Кировский завод'"},
            {"title": "Стандартизация промышленной гидравлики", "factory": "АО 'Силовые машины'"}
        ],
        "leads": [
            {"name": "Иванов Иван Игоревич (СПбПУ)", "phone": "+7 (999) 111-22-33", "course": "Работа на токарных станках ЧПУ серии ИТ-42", "status": "Заморожен"},
            {"name": "Петров Петр Георгиевич (ИТМО)", "phone": "+7 (999) 444-55-66", "course": "Стандартизация промышленной гидравлики", "status": "Заморожен"}
        ]
    }

# ==============================================================================
# 4. АРХИТЕКТУРНАЯ МОДУЛЬНОСТЬ (Логические функции вместо простыни кода)
# ==============================================================================
def render_career_hub():
    st.header("🎯 Концепт: Умный b2b-мэтчинг и Цифровой след выпускника")
    st.write("Интеллектуальный подбор молодых специалистов под нужды ОПК СПб.")
    # Здесь будет находиться или вызываться ваш старый код Варианта 1
    st.info("Модуль Кадрового хаба успешно инициализирован.")

def render_sharing_economy():
    st.header("🔬 Концепт: Шеринг свободных мощностей и оборудования НИИ")
    st.write("Промышленный маркетплейс оборудования с расчетом SLA.")
    st.info("Модуль Шеринг-экономики успешно инициализирован.")

def render_fintech_navigator():
    st.header("🎒 Концепт: Пошаговый конфигуратор промышленного обучения ребенка")
    st.write("Сконструируйте бесшовную траекторию обучения и грантов.")
    st.info("Модуль Финтех-Навигатора успешно инициализирован.")

def render_project_sm():
    """ Логика Варианта 4 для Сергея Марковича (ДПО + Финтех + Тизеры) """
    st.header("🏭 Проект С.М.: Промышленное ДПО и Лидогенерация")
    
    # Извлекаем сгруппированное состояние, чтобы не писать длинные конструкции
    data = st.session_state["sm_project"]
    
    tab_factory, tab_student, tab_marketing = st.tabs(["🏢 Кабинет Завода", "🎓 Портал Ученика", "💥 Шок-Трафик"])
    
    with tab_factory:
        st.subheader("📊 Финтех-панель управления бюджетом")
        col_bal, col_tariff = st.columns(2)
        col_bal.metric(label="Баланс расчетного счета (CPA)", value=f"{data['balance']:,.2f} руб.")
        
        tariff_status = "⚡ БЕЗЛИМИТНЫЙ ПАКЕТ" if data["is_premium"] else "🪙 ПОШТУЧНАЯ ОПЛАТА (500р/лид)"
        col_tariff.metric(label="Текущий B2B-тариф", value=tariff_status)
        
        if not data["is_premium"]:
            if st.button("🔌 Активировать полный безлимитный пакет лидов", use_container_width=True):
                data["is_premium"] = True
                st.success("Безлимитный пакет успешно подключен!")
                st.rerun()
                
        st.write("---")
        st.subheader("🎯 Поступившие кандидаты (Лиды с ДПО)")
        
        for idx, lead in enumerate(data["leads"]):
            with st.container(border=True):
                c_info, c_action = st.columns([3, 1])
                is_unlocked = data["is_premium"] or lead["status"] == "Разблокирован"
                
                c_info.write(f"**Курс ДПО:** {lead['course']}")
                c_info.write(f"**ФИО специалиста:** {lead['name'] if is_unlocked else '🔒 Данные скрыты платформой'}")
                
                if not is_unlocked:
                    if c_action.button("💳 Выкупить контакт (500 р.)", key=f"sm_buy_{idx}", use_container_width=True):
                        if data["balance"] >= 500:
                            data["balance"] -= 500
                            lead["status"] = "Разблокирован"
                            st.rerun()
                        else:
                            st.error("Недостаточно средств. Пополните баланс.")
                else:
                    c_action.write(f"📞 **{lead['phone']}**")

    with tab_student:
        st.subheader("🎓 Федеральный каталог бесплатных промышленных методик")
        for c_idx, course in enumerate(data["courses"]):
            with st.container(border=True):
                st.write(f"### 📚 {course['title']}")
                st.write(f"🏭 Индустриальный автор: **{course['factory']}**")
                if st.button("🚀 Пройти бесплатное обучение и сдать тест", key=f"stud_btn_{c_idx}"):
                    data["leads"].append({
                        "name": "Новый верифицированный выпускник",
                        "phone": "+7 (911) " + str(pd.Timestamp.now().microsecond)[:6],
                        "course": course['title'],
                        "status": "Заморожен"
                    })
                    st.success("Тест сдан! Ваша анкета передана на завод в виде лида.")
                    st.rerun()

    with tab_marketing:
        st.subheader("💥 Инструмент захвата внимания (Тизерная сеть)")
        st.error("### 🔥 ШОК! Самойлова Оксана подала в суд на Жигана из-за...")
        st.write("...из-за того, что он тайно учился на новой промышленной платформе АПП СПБ и скрыл доходы!")
        if st.button("УЗНАТЬ ПОДРОБНОСТИ И ЗАРЕГИСТРИРОВАТЬСЯ", use_container_width=True):
            st.balloons()

def render_association_audit():
    st.header("📊 Оперативный b2b/b2c-мониторинг экосистемы")
    st.write("Сквозной аудит транзакций в реальном времени.")
    # Здесь будет находиться ваш старый код Панели Ассоциации

# ==============================================================================
# 5. ИЗБЫТОЧНЫЙ РЕНДЕРИНГ (Управление потоком через словарь-маршрутизатор)
# ==============================================================================
# Создаем чистый маппинг: какая строка меню какую функцию запускает
routing_table = {
    MenuOptions.HUB: render_career_hub,
    MenuOptions.SHARING: render_sharing_economy,
    MenuOptions.NAVIGATOR: render_fintech_navigator,
    MenuOptions.PROJECT_SM: render_project_sm,
    MenuOptions.AUDIT: render_association_audit,
}

# Отрисовка сайдбара строго отделена от логики данных
selected_option = st.sidebar.radio("Выберите вариант концепции для демонстрации:", list(routing_table.keys()))

# Запуск соответствующего модуля одной строчкой
routing_table[selected_option]()
