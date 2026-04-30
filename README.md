# Breacherr - OSINT & Data Leak Tool

Вашият персонален инструмент за OSINT проучвания и проверка на изтекли данни. Проектът се състои от Python (FastAPI) бекенд и React (Vite) фронтенд, опакован като мобилно приложение чрез Capacitor.

---

## 🚀 Инструкции за стартиране от нулата

Ако искате да стартирате проекта на ново устройство, следвайте тези стъпки:

### 1. Предварителни изисквания
*   **Python 3.8+**
*   **Node.js (LTS)**
*   **Android Studio** (за мобилното приложение)

### 2. Сваляне на проекта (Git)
Отворете терминал и изпълнете:
```bash
git clone https://github.com/rivanov00/Breacherr.git
cd Breacherr
```

### 3. Настройка на Бекенда (Python)
1.  Влезте в папката на бекенда:
    ```bash
    cd backend
    ```
2.  Създайте виртуална среда:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # За Windows
    ```
3.  Инсталирайте зависимостите:
    ```bash
    pip install -r requirements.txt
    ```
4.  Стартирайте сървъра:
    ```bash
    python main.py
    ```
    *Сървърът ще работи на `http://0.0.0.0:8000`.* //това е базата данни

### 4. Настройка на Фронтенда (React)
1.  Отворете нов терминал в основната папка и влезте във фронтенда:
    ```bash
    cd frontend
    ```
2.  Инсталирайте пакетите:
    ```bash
    npm install
    ```
3.  **Важно за мобилни устройства**:
    *   Отворете `src/App.jsx` и `src/components/ReportViewer.jsx`.
    *   Намерете IP адреса (напр. `192.118.51.66`) и го заменете с актуалния IP адрес на вашия компютър в локалната мрежа. // може да го проверите чрез CMD > ipconfig > IPv4 Address
4.  Подгответе файловете за мобилното приложение:
    ```bash
    npm run build
    npx cap sync
    ```

### 4. Стартиране на Мобилното Приложение
1.  Отворете **Android Studio**.
2.  Изберете **Open Project** и посочете папка `frontend/android`.
3.  Изчакайте Gradle да завърши синхронизацията.
4.  Свържете вашия Android телефон чрез USB кабел (с активиран USB Debugging). // за да го активираш отиди в Settings > About Phone > Build Number (натисни 7 пъти) > Back > System > Developer Options > USB Debugging
5.  Натиснете бутона **Run (Play)** в Android Studio.

---

## 🛠 Технологичен стек
*   **Бекенд**: FastAPI, SQLAlchemy (SQLite), aiohttp.
*   **Фронтенд**: React, Vite, Vanilla CSS.
*   **Мобилна интеграция**: Capacitor (Native HTTP plugin за заобикаляне на CORS).

## 📁 Структура на проекта
*   `backend/core/` - Логика за OSINT сканиране и база данни.
*   `frontend/src/` - UI компоненти и логика на приложението.
*   `frontend/android/` - Нативен Android проект.
