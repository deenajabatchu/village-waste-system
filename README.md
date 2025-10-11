# Village Waste Management System

A web application to manage waste collection in villages. Villagers can raise complaints for waste collection from their homes, and admins (garbage collectors) can track and update the status of each complaint.

This project is built using **Flask, MySQL, HTML, CSS, and JavaScript**.

---

## Features

### For Villagers:
- Register and log in securely.
- Raise a complaint for waste collection.
- View the status of complaints (Pending / Collected).
- See complaints displayed in red (Pending) or green (Collected).

### For Admins:
- View all complaints from villagers.
- Mark complaints as **Collected** via dashboard.
- Status updates reflect immediately on user dashboards.
- Flash messages for success and error notifications.

---

## Technology Stack
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **Security:** Passwords hashed using `Werkzeug` (`scrypt`)

---

```plaintext
village-waste-system/
│
├─ app.py                  # Main Flask application
├─ config.py               # Database and secret key configuration
├─ schema.sql              # SQL schema for database
├─ .env                    # Environment variables (not tracked in GitHub)
├─ requirements.txt        # Python dependencies
│
├─ templates/              # HTML templates
│  ├─ base.html
│  ├─ index.html
│  ├─ register.html
│  ├─ login.html
│  ├─ raise_complaint.html
│  ├─ view_status.html
│  └─ admin_dashboard.html
│
├─ static/                 # CSS and JS files
│  ├─ css/
│  │  └─ style.css
│  └─ js/
│     └─ main.js
│
└─ README.md
