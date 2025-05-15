# 📝 Telegram Task Manager Bot

**A personal task manager Telegram bot built with Python, Aiogram, and SQLite.**  
Each user gets their own isolated task list stored in a local database.

---

## 🚀 Features

- ➕ Add tasks with deadlines  
- 📋 View your task list  
- ✅ Mark tasks as completed  
- ❌ Delete individual tasks  
- 🧹 Clear all tasks  
- 📦 Data stored in SQLite (separate table per user)

---

## 📂 Project Structure

```
project/
├── main.py                # Entry point, launches the bot
├── basic.py               # Core logic for task management
├── core/
│   └── handlers/
│       ├── basic.py       # Command handlers
│       └── callback.py    # (optional)
├── id.py                  # Token and bot/dispatcher initialization
├── user_data.db           # Task database
├── tasks.db               # Alternate task database
├── README.md              # Project description
```

---

## ⚙️ Installation & Launch

### 1. Clone the repository
```bash
git clone https://github.com/your-username/task-bot.git
cd task-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create the `id.py` file
Inside the root folder, create a file named `id.py` and add:
```python
from aiogram import Bot, Dispatcher

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)
dp = Dispatcher()
```

### 4. Run the bot
```bash
python main.py
```

---

## 📚 Available Commands

| Command     | Description                         |
|-------------|-------------------------------------|
| `/start`    | Welcome message                     |
| `/add`      | Add a new task (Format: `Task - Date`) |
| `/list`     | Show list of all tasks              |
| `/done 1`   | Mark task #1 as completed           |
| `/delete 2` | Delete task #2                      |
| `/clear`    | Clear the entire task list          |

---

## 💡 Example Task Input

```
Do the dishes - 07.12.2024 10:47
```

---

## 📌 Dependencies

- [`aiogram`](https://pypi.org/project/aiogram/) (v2.25.1 or v3+)
- `sqlite3` (built-in)

---

## 📞 Contact

**Author:** Mark  
**Telegram:** [@Markkyv](https://t.me/Markkyv)

---

> _Made with ❤️ for productivity and Telegram lovers._
