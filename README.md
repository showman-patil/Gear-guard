# 🛠️ GearGuard – Maintenance Management System

![GearGuard](https://img.shields.io/badge/Django-Full%20Stack-success)
![Status](https://img.shields.io/badge/Status-Active-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

> **GearGuard** is a modern, fully dynamic **Maintenance Management System** designed to help industries and organizations efficiently manage equipment, maintenance requests, teams, and notifications with real-time analytics.

---

## 🚀 Features

### 📊 Interactive Dashboard
- Real-time KPIs  
  - Total Equipment  
  - Maintenance Requests  
  - In-Progress Tasks  
  - Overdue Maintenance  
  - Scrap Equipment  
- Auto-refresh dashboard (every 30 seconds)

### 📈 Visual Analytics
- Doughnut chart using **Chart.js**
- Status breakdown:
  - New
  - In Progress
  - Repaired
  - Scrap
- Percentage and total request count

### 🧠 Maintenance Tracking
- Automatic overdue detection
- Upcoming preventive maintenance list
- Equipment & technician mapping

### 👥 Team Workload
- Team-wise task distribution
- Visual workload indicators
- Better resource planning

### 🔔 Notifications
- Real-time notifications
- Read / Unread status
- Mark single or all notifications as read

### ⚡ Quick Actions
- Add Equipment
- Create Maintenance Request
- Kanban / Calendar View
- Team Management
- Profile & Settings

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- Tailwind CSS
- JavaScript (ES6)
- Chart.js
- Font Awesome

### Backend
- Django
- Django REST APIs
- SQLite / PostgreSQL

---

GearGuard/
│── maintenance/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│── templates/
│ ├── dashboard.html
│── static/
│ ├── css/
│ ├── js/
│── manage.py
│── requirements.txt
│── README.md


---

## ⚙️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/your-username/gearguard.git

# Navigate to project
cd gearguard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver

➡ Open in browser: http://127.0.0.1:8000/

| Endpoint                                    | Description               |
| ------------------------------------------- | ------------------------- |
| `/maintenance/api/dashboard/`               | Dashboard KPIs & tables   |
| `/maintenance/api/kanban/`                  | Maintenance status chart  |
| `/maintenance/api/notifications/`           | Notifications list        |
| `/maintenance/api/notifications/<id>/read/` | Mark notification as read |


🎯 Use Cases

Manufacturing industries

Factory maintenance departments

IT infrastructure tracking

College / institutional labs

🧑‍💻 Developer

Rahul Patil
Full-Stack Developer
Django | Python | JavaScript

📧 Email: rahul1030patil@gmail.com

🌐 Portfolio: https://showman-patil.github.io/portfolio/

⭐ Future Enhancements

Role-based access (Admin / Technician)

Real-time updates using WebSockets

Export reports (PDF / Excel)

Mobile app integration

📜 License

This project is licensed under the MIT License.

## 📂 Project Structure

