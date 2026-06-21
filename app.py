import streamlit as st
import streamlit.components.v1 as components
import sqlite3

# Скрываем стандартные элементы оформления Streamlit, чтобы развернуть CodePen во весь экран
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0px !important; margin: 0px !important; max-width: 100% !important;}
        iframe {border: none !important; width: 100% !important; min-height: 100vh !important;}
    </style>
""", unsafe_allow_html=True)

# Имя нашей базы данных под новые расширенные поля
DB_NAME = "production_control_enterprise_v2.db"

def init_db():
    """Инициализация базы данных SQLite со всеми полями под 3 кабинета"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Таблица граждан
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citizens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT, phone TEXT, email TEXT, education TEXT,
            passport TEXT, diploma TEXT, workbook TEXT, skills TEXT,
            gdpr INTEGER DEFAULT 0, score INTEGER DEFAULT 0, status TEXT DEFAULT 'Обучение'
        )
    """)
    
    # Таблица стандартов ДПО от заводов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inn TEXT, title TEXT, model TEXT, text TEXT
        )
    """)
    
    # Таблица транзакций (подписок)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tariff TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==============================================================================
# ОБЪЕДИНЕННЫЙ КОД ИЗ CODEPEN: HTML + CSS + JS (С использованием сырой r"" строки)
# ==============================================================================
html_code = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>ПромКачество.СПб</title>
    <style>
        * { box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        body { background-color: #0B0F19 !important; color: #F8FAFC !important; margin: 0; padding: 0; }
        .cyber-app-container { display: flex; min-height: 100vh; }
        
        .cyber-sidebar {
            width: 320px; background: #0D1322; border-right: 1px solid rgba(255, 255, 255, 0.05);
            padding: 30px 20px; display: flex; flex-direction: column; justify-content: space-between;
        }
        .sidebar-header { display: flex; align-items: center; gap: 10px; }
        .cyber-sidebar h2 { font-size: 20px; font-weight: 800; color: #10B981; margin: 0; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }
        .cyber-pulse-dot { width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; box-shadow: 0 0 10px #10B981; }
        .role-selector-box label { font-size: 13px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .role-selector-box select { width: 100%; padding: 12px; background: #111827; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; color: #F8FAFC; font-weight: 600; margin-top: 8px; cursor: pointer; }
        .sidebar-footer { font-size: 12px; color: #475569; font-weight: 600; }

        .cyber-main { flex-grow: 1; padding: 30px; max-width: 1200px; }
        .hero-banner { background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important; padding: 35px; border-radius: 16px; color: #FFFFFF; margin-bottom: 25px; border-left: 8px solid #10B981; box-shadow: 0 0 25px rgba(16, 185, 129, 0.15); }
        .hero-title { font-size: 28px; font-weight: 800; background: linear-gradient(90deg, #10B981, #34D399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero-subtitle { font-size: 14px; color: #94A3B8; margin-top: 8px; line-height: 1.4; }

        .cyber-panel { display: none; width: 100%; }
        .cyber-panel h3 { font-size: 22px; font-weight: 700; color: #F8FAFC; margin-bottom: 20px; }
        .glass-form { background: rgba(17, 24, 39, 0.7); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 14px; padding: 25px; margin-bottom: 20px; backdrop-filter: blur(12px); }
        .glass-form h4 { margin-top: 0; margin-bottom: 20px; font-size: 16px; color: #34D399; font-weight: 700; }
        
        .form-grid, .form-grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px; }
        .glass-card { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px; }
        .card-title { font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; }
        
        .tariff-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .tariff-box { background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 25px; text-align: center; }
        .tariff-box.popular { border-color: #10B981; background: rgba(16, 185, 129, 0.02); box-shadow: 0 0 20px rgba(16, 185, 129, 0.05); }
        .price { font-size: 36px; font-weight: 900; color: #10B981; margin: 10px 0; }
        .desc { font-size: 13px; color: #94A3B8; }

        input, textarea, select { width: 100%; padding: 12px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: #F8FAFC; font-size: 14px; margin-bottom: 10px; }
        input:focus, textarea:focus { border-color: #10B981; outline: none; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2); }
        .question { font-weight: 600; color: #E2E8F0; }
        .radio-group label { display: block; padding: 10px; background: rgba(255, 255, 255, 0.02); margin-top: 8px; border-radius: 6px; cursor: pointer; }
        .checkbox-line { display: flex; align-items: center; gap: 8px; }
        .checkbox-line input { width: auto; margin: 0; }

        .cyber-btn, .cyber-btn-buy { background: linear-gradient(90deg, #10B981, #059669); border: none; color: white; padding: 12px 24px; font-weight: 700; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2); transition: transform 0.2s; width: 100%; }
        .cyber-btn:hover, .cyber-btn-buy:hover { transform: translateY(-2px); }

        .cyber-table-container { overflow-x: auto; }
        .cyber-table { width: 100%; border-collapse: collapse; }
        .cyber-table th, .cyber-table td { padding: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); text-align: left; }
        .cyber-table th { color: #64748B; font-size: 13px; text-transform: uppercase; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
        .badge-success { background: rgba(16, 185, 129, 0.15); color: #10B981; }
        .badge-warning { background: rgba(245, 158, 11, 0.15); color: #F59E0B; }
        .mt-3 { margin-top: 20px; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

<div class="cyber-app-container">
  <aside class="cyber-sidebar">
    <div class="sidebar-header">
      <h2>🔒 КОНТУР АПП</h2>
      <div class="cyber-pulse-dot"></div>
    </div>
    <div class="role-selector-box">
      <label>Выберите личный кабинет:</label>
      <select id="role-selector">
        <option value="citizen">&#127891; Личный кабинет Физического лица</option>
        <option value="factory">&#127981; Личный кабинет Производства</option>
        <option value="association">&#128736; Кабинет Ассоциации (Управление)</option>
      </select>
    </div>
    <div class="sidebar-footer">ПромКачество.СПб v2.0</div>
  </aside>

  <main class="cyber-main">
    <div class="hero-banner" id="cyber-banner">
      <div class="hero-title">&#127981; Промышленная экосистема опережающего ДПО «ПромКачество»</div>
      <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
    </div>

    <!-- ПАНЕЛЬ 1: ФИЗИЧЕСКИЕ ЛИЦА -->
    <section id="panel-citizen" class="cyber-panel">
      <h3>&#127891; Портал обучения и Паспорт Навыков</h3>
      <div class="glass-form">
        <h4>&#128221; Профильная анкета и загрузка документов</h4>
        <div class="form-grid">
          <input type="text" id="c_fio" placeholder="ФИО полностью" value="Иванов Игорь Игоревич">
          <input type="text" id="c_phone" placeholder="Номер телефона" value="+7(900)111-22-33">
          <input type="email" id="c_email" placeholder="E-mail" value="ivanov@spb.ru">
          <input type="text" id="c_edu" placeholder="Где учились" value="СПбПУ">
        </div>
        <div class="form-grid mt-3">
          <input type="text" id="c_pass" placeholder="Паспорт (Серия, Номер)">
          <input type="text" id="c_diploma" placeholder="Диплом (Серия, Номер)">
          <input type="text" id="c_work" placeholder="Трудовая книжка (Номер)">
        </div>
        <div style="margin-top: 15px;">
          <textarea id="c_skills" placeholder="Расскажите о ваших навыках и опыте работы..."></textarea>
        </div>
        <div class="checkbox-line">
          <input type="checkbox" id="c_gdpr" checked>
          <label for="c_gdpr">Согласие на обработку персональных данных граждан РФ</label>
        </div>
        <button class="cyber-btn" onclick="saveCitizen()">Сохранить анкету соискателя</button>
      </div>

      <div class="glass-form mt-3">
        <h4>&#129302; Тест компетенций на производстве</h4>
