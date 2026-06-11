# Daily Discipline Telegram Bot

**🇮🇷 Created in Iran**

A Telegram bot designed to help users build discipline by managing daily tasks, sleep/wake schedules, and progress tracking. The bot interface is in **Persian (Farsi)**.

## Features

### Core Features
- **Daily Task Scheduling** – Users add their daily tasks along with the estimated time needed for each task.
- **Sleep/Wake Time Management** – Users set their wake-up and sleep times. The bot starts sending task reminders from the moment they wake up.
- **Sequential Notifications** – The bot sends a notification exactly when a task should start and again when it should end, based on the user's timeline.

### Task Description & Notes
- Save a custom description for each task.
- Save personal notes and review them anytime.

### Self-Evaluation
- Users can mark which tasks were successfully completed.
- View history of completed vs. failed tasks for self-assessment.

### Friend System
- Send friend requests to other users.
- After friendship is accepted, view each other's task completion stats and profiles.

## How It Works

1. User sets wake-up time and sleep time.
2. User adds tasks with duration (e.g., "Study – 2 hours").
3. The bot automatically arranges tasks in sequence after wake-up.
4. At the scheduled start time of each task, the bot sends a reminder.
5. At the scheduled end time, the bot sends a completion reminder.
6. User evaluates each task as "done" or "failed."
7. Optional: Save notes, descriptions, and connect with friends.

## How to Run (نحوه اجرا)

Follow these steps to run the bot on your own system:

1. **Clone the repository**
   ```bash
   git clone https://github.com/nimahabibzade1/powern_bot.git
   cd powern_bot

2.**Install dependencies**
  pip install -r requirements.txt

3.**Set up environment variables**
  Open config.py and add your required environment variables. You need to add your Telegram Bot Token (obtained from @BotFather) and any other necessary keys.
  ⚠️ Important: Do not hard-code your token directly in the code. Use environment variables or a .env file for security.

4.**Create the database**
  Before running the bot for the first time, you must create the database:
  python make_database.py

5.**Run the bot**
  python main.py


**Technology Stack**
  -Python
  -python-telegram-bot (or Telebot)
  -Database (SQLite / PostgreSQL)

**Language**
  The bot interface is in Persian (Farsi).
