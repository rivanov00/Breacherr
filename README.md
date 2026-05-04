# Breacherr - OSINT & Data Leak Tool

Вашият персонален инструмент за OSINT проучвания и проверка на изтекли данни.

---

## 🛠 Използвани технологии 
*   **Бекенд**: FastAPI, SQLAlchemy (SQLite), aiohttp.
*   **Фронтенд**: React, Vite, Vanilla CSS.
*   **Мобилна интеграция**: Capacitor (Native HTTP plugin).

## 🚀 Инструкции за стартиране

### 1. Предварителни изисквания
Преди да започнете, уверете се, че имате инсталирани:
*   **Python 3.8+**
*   **Node.js (LTS версия)**
*   **Android Studio** (само ако ще ползвате мобилното приложение)
*   **Git**

### 2. Сваляне на проекта (Git)
Отворете терминал и изпълнете:
```bash
git clone https://github.com/rivanov00/Breacherr.git
cd Breacherr
```

### 3. ⚙️ Настройка на IP адреса (ЗАДЪЛЖИТЕЛНО!)
Ако сте в нова мрежа или друг потребител тества проекта, трябва да настроите вашия локален IP адрес.

**Как да намерите вашия IP адрес (Windows):**
1.  Отворете **CMD** (Start > напишете `cmd`).
2.  Въведете командата: `ipconfig`
3.  Потърсете реда **IPv4 Address** (обикновено изглежда така: `192.168.X.X`).

**Къде да смените IP адреса в проекта:**
1.  Отворете **`frontend/src/config.js`** и променете `BACKEND_IP` с вашия адрес.
2.  Отворете **`frontend/capacitor.config.json`** и променете адреса в `allowNavigation` (напр. `"192.168.X.X:8000"`).

---

### 4. Настройка на Бекенда (Python)
1.  Влезте в папката: `cd backend`
2.  Създайте виртуална среда и я активирайте:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Инсталирайте библиотеките:
    ```bash
    pip install -r requirements.txt
    ```
4.  Стартирайте сървъра:
    ```bash
    python main.py
    ```

### 5. Настройка на Фронтенда (React)
1.  Отворете нов терминал и влезте в: `cd frontend`
2.  Инсталирайте пакетите:
    ```bash
    npm install
    ```

### 6. Стартиране на приложението

#### А) В Браузър (за компютър)
1.  В терминала на `frontend` изпълнете: `npm run dev`
2.  Отворете `http://localhost:5173`

#### Б) Като Мобилно Приложение (Android)
1.  **Синхронизирайте промените** (всеки път когато сменяте IP адрес):
    ```bash
    npm run build
    npx cap sync
    ```
2.  Отворете **Android Studio**, посочете папка `frontend/android`.
3.  Свържете телефон чрез USB (с активиран **USB Debugging** от Developer Options). // Settings > About Phone > Build Number (7 пъти) > Developer Options > USB Debugging
4.  Натиснете бутона **Run (Play)**.

---
