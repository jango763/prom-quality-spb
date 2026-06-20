import streamlit as st
import pandas as pd
import random

# ==============================================================================
# ARCHITECTURAL RULE #4: Страница конфигурируется строго на первой строчке кода
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб", layout="wide", page_icon="🏭")

# ==============================================================================
# ARCHITECTURAL RULE #1 & #5: Группировка State и защита от мутации ссылок
# ==============================================================================
if "app_platform" not in st.session_state:
    st.session_state["app_platform"] = {
        "balance": 1500.00,
        "is_premium": False,
        "courses": [
            {"title": "Работа на токарных станках ЧПУ серии ИТ-42", "factory": "АО 'Кировский завод'"},
            {"title": "Стандартизация промышленной гидравлики", "factory": "АО 'Силовые машины'"}
        ],
        "leads": [
            {"name": "Иванов Иван Игоревич (СПбПУ)", "phone": "+7 (999) 111-22-33", "course": "Работа на токарных станках ЧПУ серии ИТ-42", "status": "Заморожен"},
            {"name": "Петров Пётр Георгиевич (ИТМО)", "phone": "+7 (999) 444-55-66", "course": "Стандартизация промышленной гидравлики", "status": "Заморожен"}
        ]
    }

# ==============================================================================
# ARCHITECTURAL RULE #4: Разделение монолита на изолированные бизнес-модули
# ==============================================================================

def render_factory_cabinet():
    """Модуль 1: Личный кабинет Промышленного Предприятия"""
    st.header("Управление b2b-бюджетом и кадровым резервом")
    
    col_bal, col_tariff = st.columns(2)
    col_bal.metric(label="Баланс расчетного счета предприятия (CPA)", value=f"{st.session_state['app_platform']['balance']:,.2f} руб.")
    
    tariff_status = "⚡ БЕЗЛИМИТНЫЙ ПАКЕТ ТРАФИКА" if st.session_state["app_platform"]["is_premium"] else "🪙 ПОШТУЧНАЯ ОПЛАТА (500р / готовый лид)"
    col_tariff.metric(label="Текущий B2B-тариф", value=tariff_status)
    
    if not st.session_state["app_platform"]["is_premium"]:
        if st.button("🔌 Активировать полный годовой безлимит", use_container_width=True):
            st.session_state["app_platform"]["is_premium"] = True
            st.success("Вы успешно перешли на тариф 'Безлимитный пакет'. Все контакты открыты!")
            st.rerun()
            
    st.write("---")
    st.subheader("📥 Загрузка новой методики / курса ДПО")
    
    with st.form("add_course_form"):
        new_title = st.text_input("Название инструкции или стандарта для вывода на рынок:")
        new_factory = st.text_input("Название вашего ведомства/завода:", value="АО 'Кировский завод'")
        
        if st.form_submit_button("Опубликовать методику для граждан РФ", use_container_width=True):
            # FIX #3: Строгая валидация ОБОИХ полей формы на пустые строки
            if new_title.strip() and new_factory.strip():
                st.session_state["app_platform"]["courses"].append({
                    "title": new_title.strip(), 
                    "factory": new_factory.strip()
                })
                st.success(f"Методика '{new_title}' успешно выведена в федеральный каталог!")
                st.rerun()
            else:
                st.error("Критическая ошибка: Все поля формы обязательны к заполнению!")

    st.write("---")
    st.subheader("🎯 Поступившие соискатели, обученные по вашим стандартам")
    st.info("Модель 'Итальянских поваров': эти люди умеют работать только на вашем оборудовании.")
    
    for idx, lead in enumerate(st.session_state["app_platform"]["leads"]):
        with st.container(border=True):
            c_info, c_action = st.columns()
            is_unlocked = st.session_state["app_platform"]["is_premium"] or lead["status"] == "Разблокирован"
            
            c_info.write(f"**Пройденный курс:** {lead['course']}")
            c_info.write(f"**ФИО специалиста:** {lead['name'] if is_unlocked else '🔒 Скрыто (Требуется выкуп лида)'}")
            
            if not is_unlocked:
                if c_action.button("💳 Открыть контакт (500 р.)", key=f"buy_lead_{idx}", use_container_width=True):
                    # FIX #1: Модификация состояния идет строго напрямую в сессию без посредников
                    if st.session_state["app_platform"]["balance"] >= 500:
                        st.session_state["app_platform"]["balance"] -= 500
                        st.session_state["app_platform"]["leads"][idx]["status"] = "Разблокирован"
                        st.rerun()
                    else:
                        st.error("Недостаточно средств на балансе CPA. Пополните счет.")
            else:
                c_action.write(f"📞 **{lead['phone']}**")


def render_student_portal():
    """Модуль 2: Федеральный Портал ДПО для Граждан"""
    st.header("Бесплатное профессиональное обучение и быстрый старт в ОПК")
    st.write("Выберите сертифицированную методику завода, пройдите интерактивный тест и получите гарантированный контракт.")
    
    for c_idx, course in enumerate(st.session_state["app_platform"]["courses"]):
        with st.container(border=True):
            st.subheader(f"📚 {course['title']}")
            st.write(f"🏭 Разработчик стандарта и оборудования: **{course['factory']}**")
            
            if st.button("🚀 Начать изучение курса и сдать тест", key=f"start_course_{c_idx}"):
                # FIX #2: Замена ломающихся микросекунд на безопасный генератор случайного номера телефона
                random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
                safe_phone = f"+7 (911) {random_digits[:3]}-{random_digits[3:5]}-{random_digits[5:]}"
                
                # FIX #1: Прямая запись нового лида в сессию для предотвращения сброса UI
                st.session_state["app_platform"]["leads"].append({
                    "name": f"Новый верифицированный выпускник №{random.randint(100, 999)}",
                    "phone": safe_phone,
                    "course": course['title'],
                    "status": "Заморожен"
                })
                st.balloons()
                st.success("Поздравляем! Вы успешно изучили методику. Ваша анкета передана на завод.")
                st.rerun()


def render_marketing_tool():
    """Модуль 3: Инструмент Вирусного Трафика"""
    st.header("Инструмент захвата внимания половины граждан РФ")
    st.write("Генератор шок-контента для агрессивного привлечения бесплатного b2c-трафика.")
    
    with st.container(border=True):
        st.error("### 🔥 ШОК! Самойлова Оксана подала в суд на Жигана из-за...")
        st.write("...из-за того, что он тайно от неё прошел бесплатное промышленное ДПО на платформе АПП Санкт-Петербурга, устроился на завод и скрыл миллионные доходы!")
        st.write("👇 👇 👇")
        if st.button("УЗНАТЬ ПОДРОБНОСТИ И ЗАРЕГИСТРИРОВАТЬСЯ БЕСПЛАТНО", use_container_width=True):
            st.toast("Клик засчитан! Пользователь перенаправлен на вкладку обучения.")

# ==============================================================================
# ТОЧКА ВХОДА (MAIN RUNNER)
# ==============================================================================
st.title("🏭 Цифровая экосистема «ПромКачество.СПб»")
st.caption("Официальная b2b/b2c-платформа Ассоциации промышленных производств Санкт-Петербурга")

# Рендеринг вкладок верхнего уровня через модульные функции
tab_factory, tab_student, tab_marketing = st.tabs([
    "🏢 Кабинет Промышленного Предприятия (Завод)", 
    "🎓 Портал ДПО (Гражданин)", 
    "💥 Вирусный Трафик (Тизерная Сеть)"
])

with tab_factory:
    render_factory_cabinet()

with tab_student:
    render_student_portal()

with tab_marketing:
    render_marketing_tool()
