# 🎓 Placement Portal

A full-stack college placement management system built with **Flask** (backend) and **Vue.js** (frontend). It connects students, companies, and admins on a single platform to streamline the campus recruitment process.

---

## 📌 Features

### 👨‍🎓 Student
- Register and create a profile (branch, CGPA, education level, GitHub, LinkedIn)
- View eligible placement drives (auto-filtered by CGPA, branch, year, education level)
- Apply to open drives with a single click
- Track application status (Applied → Shortlisted → Selected / Rejected)
- Update profile details (contact, CGPA, GitHub, LinkedIn)
- Export applications as CSV (async via Celery)

### 🏢 Company
- Register and await admin approval
- Create placement drives with detailed eligibility criteria
- View list of applicants per drive
- Shortlist, select, or reject applicants

### 🛡️ Admin
- Dashboard with platform-wide statistics
- Approve or reject company registrations
- Approve or reject placement drives
- Blacklist / unblacklist students or companies
- Receive CSV export of all applications via email

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, Vue Router, Pinia, Vite |
| Backend | Flask, Flask-Security-Too, Flask-SQLAlchemy |
| Database | SQLite |
| Async Tasks | Celery + Redis |
| Email | Flask-Mail (SMTP) |
| Auth | Token-based (Flask-Security auth tokens) |

---

## 📁 Project Structure

```
mad2-project/
├── backend/
│   ├── controllers/
│   │   ├── __init__.py          # App factory, DB init, role seeding
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── database.py          # DB instance
│   │   ├── user_datastore.py    # Flask-Security datastore
│   │   ├── auth.py              # Auth routes (register/login/logout)
│   │   ├── admin.py             # Admin routes
│   │   ├── student.py           # Student routes
│   │   └── company.py           # Company routes
│   ├── celery_app.py            # Celery tasks (CSV export, email reminders)
│   ├── mail.py                  # Email helper
│   ├── main.py                  # App entry point
│   ├── data.csv                 # Sample/exported CSV
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── views/
    │   │   ├── auth/            # Login, StudentRegister, CompanyRegister
    │   │   ├── admin/           # AdminDashboard, Companies, Students, Drives
    │   │   ├── student/         # Dashboard, Drives, Applications, Profile
    │   │   └── company/         # Dashboard, Drives, CreateDrive, Applicants
    │   ├── components/
    │   │   ├── PrivateNavbar.vue
    │   │   └── PublicNavbar.vue
    │   ├── stores/
    │   │   └── auth.js          # Pinia auth store
    │   ├── router/
    │   │   └── index.js         # Vue Router config
    │   ├── App.vue
    │   └── main.js
    ├── index.html
    └── vite.config.js
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Redis (for Celery)

---

### 🔧 Backend Setup

```bash
# Navigate to backend
cd mad2-project/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python main.py
```

The backend runs at `http://localhost:5000`

> **Default Admin Credentials**
> - Email: `admin@gmail.com`
> - Password: `Admin@123`

---

### 🎨 Frontend Setup

```bash
# Navigate to frontend
cd mad2-project/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend runs at `http://localhost:5173`

---

### ⚡ Celery Worker (for async tasks)

Make sure Redis is running, then in a separate terminal:

```bash
cd mad2-project/backend

# Start Celery worker
celery -A celery_app worker --loglevel=info

# Start Celery beat scheduler (for periodic tasks)
celery -A celery_app beat --loglevel=info
```

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/student/register` | Register a new student |
| POST | `/company/register` | Register a new company |
| POST | `/login` | Login (returns auth token) |
| POST | `/logout` | Logout |

### Admin *(requires admin token)*
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Platform stats |
| GET | `/admin/companies` | List all companies |
| POST | `/admin/company/approve/<id>` | Approve company |
| POST | `/admin/company/reject/<id>` | Reject company |
| GET | `/admin/students` | List all students |
| POST | `/admin/blacklist/<user_id>` | Blacklist a user |
| POST | `/admin/unblacklist/<user_id>` | Unblacklist a user |
| GET | `/admin/drives` | List all drives |
| POST | `/admin/drive/approve/<id>` | Approve drive |
| POST | `/admin/drive/reject/<id>` | Reject drive |

### Student *(requires student token)*
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/student/dashboard` | Student stats |
| GET | `/student/drives` | View eligible drives |
| POST | `/student/apply/<drive_id>` | Apply to a drive |
| GET | `/student/applications` | View own applications |
| PUT | `/student/profile` | Update profile |
| GET | `/export-csv` | Trigger CSV export (async) |

### Company *(requires company token)*
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/company/dashboard` | Company stats |
| POST | `/company/create-drive` | Create a placement drive |
| GET | `/company/drives` | View own drives |
| GET | `/company/applications/<drive_id>` | View applicants for a drive |
| POST | `/company/shortlist/<application_id>` | Shortlist a student |
| POST | `/company/select/<application_id>` | Select a student |
| POST | `/company/reject/<application_id>` | Reject a student |

---

## 🗄️ Database Models

```
User ──< UserRoles >── Role
 │
 ├── StudentProfile ──< Application >── PlacementDrive ──< CompanyProfile
 └── CompanyProfile
```

- **User** — core auth entity with role-based access and blacklist support
- **StudentProfile** — academic details tied to a user
- **CompanyProfile** — company info with admin approval workflow
- **PlacementDrive** — job listing with eligibility criteria
- **Application** — many-to-many between students and drives, with status tracking

---

## 📋 Application Status Flow

```
Student Applies → Applied
                     │
            Company Reviews
           /               \
     Shortlisted          Rejected
          │
     Selected / Rejected
```

---

## 🔐 Authentication

All protected routes use **token-based authentication** via Flask-Security. After login, include the token in request headers:

```
Authentication-Token: <your_token_here>
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)
```
flask
flask_sqlalchemy
flask_security_too
flask_restful
flask-cors
celery
```

### Frontend (`package.json`)
- vue, vue-router, pinia
- vite, @vitejs/plugin-vue

---

## 🚀 Future Improvements

- [ ] JWT-based authentication
- [ ] Resume upload support for students
- [ ] Email notifications on application status change
- [ ] Advanced search and filter for drives
- [ ] Analytics dashboard with charts
- [ ] Docker support for easy deployment

---

## 👨‍💻 Author

Built as part of the **MAD-2 (Modern Application Development 2)** course project.

---

## 📄 License

This project is for educational purposes. Feel free to fork and build upon it.
