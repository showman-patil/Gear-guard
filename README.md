🛠️ GearGuard – Maintenance Management System






GearGuard ek smart, modern aur fully dynamic maintenance management system hai jo industries, factories aur organizations ko equipment maintenance, team workload, notifications aur analytics efficiently manage karne me madad karta hai.

🚀 Features
📊 Interactive Dashboard

Real-time KPIs

Total Equipment

Maintenance Requests

In-Progress Tasks

Overdue Maintenance

Scrap Equipment

Auto-refresh dashboard (every 30 seconds)

📈 Visual Analytics

Doughnut Chart using Chart.js

Maintenance Status:

New

In Progress

Repaired

Scrap

Percentage + total count visualization

🧠 Smart Maintenance Tracking

Overdue maintenance detection

Upcoming preventive maintenance list

Technician & equipment mapping

👥 Team Workload Management

Team-wise task distribution

Visual workload bars

Better resource planning

🔔 Notification System

Real-time notifications

Read / Unread status

Mark individual or all notifications as read

⚡ Quick Actions

Add Equipment

Create Maintenance Request

View Calendar (Kanban Board)

Team Management

Profile & Settings

🛠️ Tech Stack
Frontend

HTML5

Tailwind CSS

JavaScript (ES6)

Chart.js

Font Awesome

Backend

Django

Django REST APIs

SQLite / PostgreSQL

📂 Project Structure
GearGuard/
│── maintenance/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│── templates/
│   ├── dashboard.html
│── static/
│   ├── js/
│   ├── css/
│── manage.py
│── requirements.txt
│── README.md

⚙️ Installation & Setup
# Clone the repository
git clone https://github.com/your-username/gearguard.git

# Navigate to project
cd gearguard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver


➡ Open browser: http://127.0.0.1:8000/

🔄 API Endpoints
Endpoint	Description
/maintenance/api/dashboard/	Dashboard KPIs & tables
/maintenance/api/kanban/	Chart status data
/maintenance/api/notifications/	Notifications list
/maintenance/api/notifications/<id>/read/	Mark notification read
📸 Screenshots (Optional)

Add screenshots here to make README more attractive

/screenshots/dashboard.png
/screenshots/chart.png

🎯 Use Cases

Manufacturing industries

IT infrastructure maintenance

Factory equipment tracking

College / Institutional labs

🧑‍💻 Developer

Rahul Patil

Full-Stack Developer

Django | Python | JavaScript

Passionate about clean UI & scalable systems

📧 Email: rahul1030patil@gmail.com

🌐 Portfolio: https://showman-patil.github.io/portfolio/

⭐ Future Enhancements

Role-based access (Admin / Technician)

WebSockets for real-time updates

PDF & Excel report export

Mobile app integration

📜 License

This project is licensed under the MIT License
You are free to use, modify and distribute it.
