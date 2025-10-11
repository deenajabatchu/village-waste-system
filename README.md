# village-waste-system

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



**Clone the repository:**

```bash
git clone https://github.com/deenajabatchu/village-waste-system.git
cd village-waste-system
