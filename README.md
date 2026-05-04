# Breacherr - OSINT & Data Leak Tool

Вашият персонален инструмент за OSINT проучвания и проверка на изтекли данни.

---

## 🚀 Инструкции за стартиране

### 1. Предварителни изисквания
Преди да започнете, уверете се, че имате инсталирани:
*   **Python 3.13+**
*   **Node.js - изтеглете от тук https://nodejs.org/en/download** 
*   **Android Studio - изтеглете от тук https://developer.android.com/studio** (само ако ще ползвате мобилното приложение)

### 2. Сваляне на проекта (Git)
Отворете терминал и изпълнете:
```bash
Свалете проекта от https://github.com/rivanov00/Breacherr.git в ZIP (Code > Download ZIP)
Разархивирайте го и влезте в него с вашето IDE (Visual studio, windsurf, antigravity и т.н.)
```

### 3. ⚙️ Настройка на IP адреса (ЗАДЪЛЖИТЕЛНО!)
Ако сте в нова мрежа или друг потребител тества проекта, трябва да настроите вашия локален IP адрес.

**Намиране на вашия IP адрес (Windows):**
1.  Отворете **CMD** (Start > напишете `cmd`).
2.  Въведете командата: `ipconfig`
3.  Потърсете реда **IPv4 Address** (обикновенно изглежда така: `192.168.X.X`).

**Смяна на IP адреса в проекта:**
1.  Отворете **`frontend/src/config.js`** и променете `BACKEND_IP` с вашия адрес.
2.  Отворете **`frontend/capacitor.config.json`** и променете адреса в `allowNavigation` (напр. `"192.168.X.X:8000"`).

---

### 4. Стартиране на Бекенда (Python)
1. Отворете терминал в папката на проекта и направете виртуална среда, за да не инсталирате библиотеки директно на компютъра си
   ```bash
   python -m venv .venv
   ```
2. Влезте в папката на бекенда:
   ```bash
   cd backend
   ```
3. (Ако стартирате за първи път) Инсталирайте библиотеките:
   ```bash
   pip install -r requirements.txt
   ```
4. Стартирайте сървъра:
   ```bash
   python main.py
   ```

### 5. Стартиране на Фронтенда (React)
1. Отворете **нов терминал** в папката на проекта.
2. Влезте в папката на фронтенда:
   ```bash
   cd frontend
   ```
3. Инсталирайте пакетите(ако дава грешка, уверете се, че е инсталиран Node.js):
   ```bash
   npm install
   ```
4. Стартирайте приложението:
   ```bash
   npm run dev
   ```
5. Отворете в браузъра: `http://localhost:5173`

### 6. Стартиране на Мобилно Приложение (Android)

1.  **Синхронизирайте промените** Ако сте сменил IP address, отворете нов терминал в папката на проекта и напишете следните команди:
    ```bash
    npm run build
    npx cap sync
    ```
2.  Отворете **Android Studio**, посочете папка `frontend/android`.
3.  Свържете телефон чрез USB кабел който поддържа Data Transfer (с активиран **USB Debugging** от Developer Options). // Settings > About Phone > Build Number (7 пъти) > Developer Options > USB Debugging
4.  Натиснете бутона **Run (Play)**.
5. Това ще зареди приложението на вашето Android устройство.


## 🛠 Използвани технологии 
*   **Бекенд**: FastAPI, SQLAlchemy (SQLite), aiohttp.
*   **Фронтенд**: React, Vite, Vanilla CSS.
*   **Мобилна интеграция**: Capacitor (Native HTTP plugin).


---