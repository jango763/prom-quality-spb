<div class="cyber-app-container">
  
  <!-- Сайдбар управления ролями -->
  <aside class="cyber-sidebar">
    <div class="sidebar-header">
      <h2>🔒 КОНТУР АПП</h2>
      <div class="cyber-pulse-dot"></div>
    </div>
    <div class="role-selector-box">
      <label>Выберите личный кабинет:</label>
      <select id="role-selector">
        <option value="citizen">🎓 Личный кабинет Физического лица</option>
        <option value="factory">🏢 Личный кабинет Производства</option>
        <option value="association">🛠️ Кабинет Ассоциации (Управление)</option>
      </select>
    </div>
    <div class="sidebar-footer">ПромКачество.СПб v2.0</div>
  </aside>

  <!-- Главный контентный блок -->
  <main class="cyber-main">
    
    <!-- Наш особый премиум Hero-баннер -->
    <div class="hero-banner" id="cyber-banner">
      <div class="hero-glow-effect"></div>
      <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
      <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
      <div class="cyber-pulse-bar"></div>
    </div>

    <!-- ========================================== -->
    <!-- КОНТУР 1: ФИЗИЧЕСКИЕ ЛИЦА (ПАНЕЛЬ СОИСКАТЕЛЯ) -->
    <!-- ========================================== -->
    <section id="panel-citizen" class="cyber-panel">
      <h3>🎓 Портал обучения и Паспорт Навыков</h3>
      
      <div class="glass-form">
        <h4>📝 Профильная анкета и загрузка документов</h4>
        <div class="form-grid">
          <input type="text" placeholder="ФИО полностью" value="Иванов Игорь Игоревич">
          <input type="text" placeholder="Номер телефона" value="+7(900)111-22-33">
          <input type="email" placeholder="E-mail" value="ivanov@spb.ru">
          <input type="text" placeholder="Где учились" value="СПбПУ">
        </div>
        <div class="form-grid mt-3">
          <input type="text" placeholder="Паспорт (Серия, Номер)">
          <input type="text" placeholder="Диплом (Серия, Номер)">
          <input type="text" placeholder="Трудовая книжка (Номер)">
        </div>
        <div class="textarea-box mt-3">
          <textarea placeholder="Расскажите о ваших навыках и опыте работы..."></textarea>
        </div>
        <div class="checkbox-line mt-3">
          <input type="checkbox" id="gdpr">
          <label for="gdpr">Согласие на обработку персональных данных граждан РФ</label>
        </div>
        <button class="cyber-btn mt-3">Сохранить анкету соискателя</button>
      </div>

      <div class="glass-form mt-3">
        <h4>🤖 Тест компетенций на производстве</h4>
        <p class="question">Критическая аварийная ситуация: Датчик стойки управления Syntec выдал перегрев шпинделя станка ЧПУ за 20 млн рублей. Ваши действия?</p>
        <div class="radio-group">
          <label><input type="radio" name="q1"> Игнорировать и закончить деталь</label>
          <label><input type="radio" name="q1"> Нажать аварийную кнопку STOP, перекрыть СОЖ и вызвать мастера</label>
          <label><input type="radio" name="q1"> Снизить обороты шпинделя вручную на 20%</label>
        </div>
        <button class="cyber-btn mt-3">Отправить ответы экзамена</button>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- КОНТУР 2: ЮРИДИЧЕСКИЕ ЛИЦА (ПАНЕЛЬ ЗАВОДА) -->
    <!-- ========================================== -->
    <section id="panel-factory" class="cyber-panel">
      <h3>🏢 Кабинет Завода-Производителя оборудования</h3>
      
      <div class="form-grid-3">
        <div class="glass-card">
          <div class="card-title">ТЕКУЩИЙ ТАРИФ</div>
          <div class="card-value">ПОШТУЧНЫЙ ВЫКУП</div>
        </div>
        <div class="glass-card">
          <div class="card-title">ОСТАТОК АНКЕТ</div>
          <div class="card-value" style="color: #3B82F6;">5 ШТ.</div>
        </div>
        <div class="glass-card">
          <div class="card-title">БЕЗЛИМИТНЫЙ ДОСТУП</div>
          <div class="card-value" style="color: #EF4444;">❌ ВЫКЛ.</div>
        </div>
      </div>

      <div class="glass-form mt-3">
        <h4>💳 Тарифная сетка и покупка лицензии</h4>
        <div class="tariff-grid">
          <div class="tariff-box">
            <h5>📦 Штучный пакет</h5>
            <p class="price">15 000 ₽</p>
            <p class="desc">Доступ к 5 проверенным анкетам соискателей</p>
            <button class="cyber-btn-buy">Купить пакет</button>
          </div>
          <div class="tariff-box popular">
            <h5>⚔️ Безлимитный Год</h5>
            <p class="price">150 000 ₽</p>
            <p class="desc">Полный безлимит на выгрузку "Железных мастеров"</p>
            <button class="cyber-btn-buy">Активировать Безлимит</button>
          </div>
        </div>
      </div>

      <div class="glass-form mt-3">
        <h4>📥 Загрузка b2b-стандарта ДПО</h4>
        <div class="form-grid">
          <input type="text" placeholder="ИНН предприятия">
          <input type="text" placeholder="Название программы обучения">
          <input type="text" placeholder="Модель промышленного станка">
        </div>
        <div class="textarea-box mt-3">
          <textarea placeholder="Введите развернутые пошаговые инструкции и регламенты безопасности..."></textarea>
        </div>
        <button class="cyber-btn mt-3">Опубликовать стандарт завода</button>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- КОНТУР 3: АССОЦИАЦИЯ (ПАНЕЛЬ УПРАВЛЕНИЯ) -->
    <!-- ========================================== -->
    <section id="panel-association" class="cyber-panel">
      <h3>🛠️ Пульт Оперативного Контроля АПП СПб</h3>
      
      <div class="form-grid-3">
        <div class="glass-card">
          <div class="card-title">ВСЕГО ФИЗИКОВ</div>
          <div class="card-value">1,420</div>
        </div>
        <div class="glass-card">
          <div class="card-title">ВСЕГО ПРОИЗВОДСТВ</div>
          <div class="card-value" style="color: #3B82F6;">86</div>
        </div>
        <div class="glass-card">
          <div class="card-title">ОБЩАЯ СУММА ОПЛАТ</div>
          <div class="card-value" style="color: #F59E0B;">165 000 ₽</div>
        </div>
      </div>

      <div class="glass-form mt-3">
        <h4>📊 Аудит транзакций и статуса подписок</h4>
        <div class="cyber-table-container">
          <table class="cyber-table">
            <thead>
              <tr>
                <th>Предприятие</th>
                <th>ИНН</th>
                <th>Тип оплаты</th>
                <th>Сумма</th>
                <th>Статус подписки</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>АО «Кировский завод»</td>
                <td>7805041230</td>
                <td>Безлимит (Год)</td>
                <td style="color:#10B981; font-weight:700;">150 000 ₽</td>
                <td><span class="badge badge-success">Активна</span></td>
              </tr>
              <tr>
                <td>ПАО «Силовые машины»</td>
                <td>7804014560</td>
                <td>Поштучно (5 шт)</td>
                <td style="color:#10B981; font-weight:700;">15 000 ₽</td>
                <td><span class="badge badge-warning">Лимит</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

  </main>
</div>
script.js
document.addEventListener("DOMContentLoaded", function() {
    const roleSelector = document.getElementById("role-selector");
    
    if (roleSelector) {
        function switchPanel(targetRole) {
            const panelIds = ['panel-citizen', 'panel-factory', 'panel-association'];
            
            panelIds.forEach(id => {
                const panel = document.getElementById(id);
                if (panel) {
                    if (id === `panel-${targetRole}`) {
                        panel.style.setProperty('display', 'block', 'important');
                        panel.classList.add("active");
                    } else {
                        panel.style.setProperty('display', 'none', 'important');
                        panel.classList.remove("active");
                    }
                }
            });
        }

        roleSelector.addEventListener("change", function(e) {
            switchPanel(e.target.value);
        });

        // Первичный запуск
        switchPanel(roleSelector.value);
    }
});
style.css
/* ==============================================================================
   ФИНАЛЬНЫЙ ПРЕМИУМ-ДИЗАЙН СИСТЕМЫ АПП СПБ
   ============================================================================== */
* {
    box-sizing: border-box;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

body {
    background-color: #0B0F19 !important;
    color: #F8FAFC !important;
    margin: 0;
    padding: 0;
}

.cyber-app-container {
    display: flex;
    min-height: 100vh;
}

/* Стилизация сайдбара */
.cyber-sidebar {
    width: 320px;
    background: #0D1322;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    padding: 30px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 10px;
}

.cyber-sidebar h2 {
    font-size: 20px;
    font-weight: 800;
    color: #10B981;
    margin: 0;
    text-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
}

.cyber-pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10B981;
}

.role-selector-box label {
    font-size: 13px;
    color: #94A3B8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.role-selector-box select {
    width: 100%;
    padding: 12px;
    background: #111827;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 8px;
    color: #F8FAFC;
    font-weight: 600;
    margin-top: 8px;
    cursor: pointer;
}

.sidebar-footer {
    font-size: 12px;
    color: #475569;
    font-weight: 600;
}

/* Главный блок контента */
.cyber-main {
    flex-grow: 1;
    padding: 30px;
    max-width: 1200px;
}

/* Наш особый неоновый Hero-баннер */
.hero-banner {
    background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important;
    padding: 35px;
    border-radius: 16px;
    color: #FFFFFF;
    margin-bottom: 25px;
    border-left: 8px solid #10B981;
    box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
}

.hero-title {
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(90deg, #10B981, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 14px;
    color: #94A3B8;
    margin-top: 8px;
    line-height: 1.4;
}

/* Панели кабинетов */
.cyber-panel {
    display: none;
    width: 100%;
    animation: fadeIn 0.4s ease-in-out forwards;
}

.cyber-panel h3 {
    font-size: 22px;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 20px;
}

/* Стеклянные матовые контейнеры (Glassmorphism) */
.glass-form {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 25px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
}

.glass-form h4 {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 16px;
    color: #34D399;
    font-weight: 700;
}

.form-grid, .form-grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 15px;
}

/* Объемные b2b карточки тарифов и KPI */
.glass-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
}

.card-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-value {
    font-size: 24px;
    font-weight: 800;
    color: #10B981;
    margin-top: 5px;
}

/* Тарифная сетка */
.tariff-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.tariff-box {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 25px;
    text-align: center;
}

.tariff-box.popular {
    border-color: #10B981;
    background: rgba(16, 185, 129, 0.02);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.05);
}

.tariff-box h5 {
    font-size: 18px;
    margin: 0 0 10px 0;
}

.price {
    font-size: 36px;
    font-weight: 900;
    color: #10B981;
    margin: 10px 0;
}

.desc {
    font-size: 13px;
    color: #94A3B8;
}

/* Поля ввода */
input, textarea, select {
    width: 100%;
    padding: 12px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: #F8FAFC;
    font-size: 14px;
}

input:focus, textarea:focus {
    border-color: #10B981;
    outline: none;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
}

.question {
    font-weight: 600;
    color: #E2E8F0;
}

.radio-group label {
    display: block;
    padding: 10px;
    background: rgba(255, 255, 255, 0.02);
    margin-top: 8px;
    border-radius: 6px;
    cursor: pointer;
}

.checkbox-line {
    display: flex;
    align-items: center;
    gap: 8px;
}
.checkbox-line input {
    width: auto;
}

/* Кнопки */
.cyber-btn, .cyber-btn-buy {
    background: linear-gradient(90deg, #10B981, #059669);
    border: none;
    color: white;
    padding: 12px 24px;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    transition: transform 0.2s;
}

.cyber-btn:hover, .cyber-btn-buy:hover {
    transform: translateY(-2px);
}

/* Таблицы */
.cyber-table-container {
    overflow-x: auto;
}

.cyber-table {
    width: 100%;
    border-collapse: collapse;
}

.cyber-table th, .cyber-table td {
    padding: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    text-align: left;
}

.cyber-table th {
    color: #64748B;
    font-size: 13px;
    text-transform: uppercase;
}

.badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
}
.badge-success { background: rgba(16, 185, 129, 0.15); color: #10B981; }
.badge-warning { background: rgba(245, 158, 11, 0.15); color: #F59E0B; }

.mt-3 { margin-top: 20px; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
