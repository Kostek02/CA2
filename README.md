# Secure Notes Web Application

**Name:** Konstanty Litwinow  
**Student ID:** 23437073  
**Programme:** MSc Cybersecurity  
**Module:** Secure Web Development (H9SWD)  
**Assessment:** CA2 - Secure Web Application  
**Framework:** Flask (Python 3.9+)  
**Repository:** [https://github.com/Kostek02/CA2](https://github.com/Kostek02/CA2)

---

## Project Title and Overview

The **Secure Notes Web Application** is a production-ready, security-hardened note management system built with Flask. This application demonstrates the **Secure Software Development Lifecycle (SSDLC)** by evolving from an intentionally insecure baseline to a fully hardened web application that addresses all OWASP Top 10 2025 vulnerabilities.

**Primary Purpose:**
- Provide a secure platform for users to create, manage, and organize personal notes
- Demonstrate enterprise-level security practices and secure coding principles
- Showcase the complete security hardening process from vulnerable to production-ready

**Main Security Focus:**
The application implements comprehensive security controls including SQL injection prevention, CSRF protection, role-based access control (RBAC), secure authentication, input validation, security headers, rate limiting, and comprehensive audit logging.

---

## Features and Security Objectives

### Major Functionalities

1. **User Authentication**
   - User registration with password strength requirements
   - Secure login with rate limiting
   - Session management with secure cookies
   - Logout functionality

2. **Note Management (CRUD Operations)**
   - Create new notes with title and content
   - View personal notes (or all notes for moderators/admins)
   - Edit existing notes (ownership-based or admin override)
   - Delete notes (ownership-based or moderator/admin override)

3. **Role-Based Access Control (RBAC)**
   - **User Role:** Can create, view, edit, and delete only their own notes
   - **Moderator Role:** Can view all notes, edit own notes, delete any note (moderation power)
   - **Admin Role:** Full access to all notes and admin dashboard with user/note management

4. **Admin Dashboard**
   - View all users in the system
   - View all notes with user associations
   - Access restricted to admin role only

### Security Improvements Implemented

1. **SQL Injection Prevention (A05 - Injection)**
   - ✅ All database queries use parameterized statements
   - ✅ 100% elimination of SQL injection vulnerabilities (11 Bandit, 13 Semgrep → 0)

2. **CSRF Protection (A05 - Injection)**
   - ✅ Flask-WTF CSRF tokens on all forms
   - ✅ Token validation on all POST requests

3. **Secure Authentication (A07 - Authentication Failures)**
   - ✅ bcrypt password hashing (no plaintext storage)
   - ✅ Flask-Login secure session management
   - ✅ Rate limiting on login/register (3-5 attempts per minute)

4. **Broken Access Control Mitigation (A01 - Broken Access Control)**
   - ✅ RBAC with role-based decorators
   - ✅ Ownership validation on all note operations
   - ✅ Admin-only routes protected with `@admin_required`

5. **Input Validation and Sanitization (A05 - Injection)**
   - ✅ WTForms validation on all user inputs
   - ✅ Length constraints and data type validation
   - ✅ Username uniqueness checks

6. **Security Headers (A02 - Security Misconfiguration)**
   - ✅ Content Security Policy (CSP)
   - ✅ HTTP Strict Transport Security (HSTS)
   - ✅ X-Frame-Options: DENY
   - ✅ X-Content-Type-Options: nosniff

7. **Audit Logging (A09 - Logging & Alerting Failures)**
   - ✅ Comprehensive logging of all authentication events
   - ✅ CRUD operation logging with user context
   - ✅ Error logging for security events
   - ✅ Log rotation to prevent disk exhaustion

8. **Error Management (A10 - Mishandling of Exceptional Conditions)**
   - ✅ Custom error handlers (403, 404, 429, 500)
   - ✅ Secure error messages (no information leakage)
   - ✅ Error logging for debugging

---

## Project Structure

```
CA2/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory
│   ├── auth/                    # Authentication blueprint
│   │   ├── routes.py            # Registration, login, logout routes
│   │   ├── forms.py             # WTForms for auth (CSRF protection)
│   │   └── models.py            # User model for Flask-Login
│   ├── notes/                   # Notes blueprint
│   │   ├── routes.py            # CRUD operations for notes
│   │   └── forms.py             # Note form with validation
│   ├── admin/                   # Admin blueprint
│   │   └── routes.py            # Admin dashboard (admin-only)
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html            # Base template
│   │   ├── home.html            # Homepage
│   │   ├── auth/                # Authentication templates
│   │   ├── notes/               # Notes templates
│   │   └── admin/               # Admin templates
│   ├── static/                  # Static assets
│   │   └── css/
│   │       └── main.css         # Application styles
│   ├── db.py                    # Database connection helper
│   ├── rbac.py                  # Role-based access control helpers
│   ├── audit.py                 # Audit logging utilities
│   └── error_handlers.py        # Custom error handlers
│
├── docs/                        # Documentation
│   ├── prd.md                   # Product Requirements Document
│   ├── dev_plan.md              # Development plan with phases
│   └── evidence/                # Testing evidence and reports
│       ├── bandit-v1.4-report.txt    # Baseline SAST report
│       ├── bandit-v2.4-report.txt     # Final SAST report
│       ├── semgrep-v1.5-report.json   # Baseline Semgrep report
│       ├── semgrep-v2.4-report.json   # Final Semgrep report
│       └── v2.4-comparison-report.md  # Before/after comparison
│
├── tests/                       # Test suite
│   ├── test_auth.py             # Authentication tests
│   ├── test_notes.py            # Notes CRUD tests
│   └── test_admin.py            # Admin access tests
│
├── instance/                     # Instance-specific files
│   ├── schema.sql               # Database schema
│   └── secure_notes.db          # SQLite database (created on first run)
│
├── logs/                        # Application logs
│   ├── audit.log                # Security event logs
│   └── error.log                # Error logs
│
├── config.py                    # Configuration management
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── run_app.sh                   # macOS/Linux startup script
├── run_app.ps1                  # Windows PowerShell startup script
├── .env                         # Environment variables (not in repo)
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

### Key Files Explained

- **`app/__init__.py`**: Flask application factory that initializes the app, registers blueprints, configures Flask-Talisman (security headers), Flask-Limiter (rate limiting), and Flask-Login (session management)
- **`app/auth/routes.py`**: Handles user registration, login, and logout with bcrypt password hashing and rate limiting
- **`app/notes/routes.py`**: Implements CRUD operations for notes with RBAC and ownership checks
- **`app/rbac.py`**: Provides decorators (`@admin_required`, `@moderator_required`) and helper functions for access control
- **`app/audit.py`**: Centralized logging system for authentication events, CRUD operations, and errors
- **`config.py`**: Manages configuration from environment variables with secure defaults
- **`run_app.sh` / `run_app.ps1`**: Convenience scripts to set up virtual environment and run the application

---

## Setup and Installation Instructions

### Prerequisites

- **Python 3.9+** (tested with Python 3.9.6)
- **SQLite** (preinstalled on macOS/Linux, included with Python on Windows)
- **Git** (for cloning the repository)

### Installation Steps

#### Option 1: Using the Provided Scripts (Recommended)

**macOS / Linux:**
```bash
# Make the script executable
chmod +x run_app.sh

# Run the script (it will create venv, install dependencies, and start the app)
./run_app.sh
```

**Windows (PowerShell):**
```powershell
# Set execution policy (if needed, run once)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the script
.\run_app.ps1
```

The scripts will automatically:
1. Create a Python virtual environment (`venv/`)
2. Install all dependencies from `requirements.txt`
3. Initialize the database (if not exists)
4. Start the Flask development server

#### Option 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/Kostek02/CA2.git
cd CA2

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Edit .env and set SECRET_KEY (generate a random string)

# 6. Initialize database
flask init-db

# 7. Run the application
python run.py
```

### Configuration

1. **Environment Variables**: Copy `.env.example` to `.env` and configure:
   - `SECRET_KEY`: A random string for Flask session encryption (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `FLASK_ENV`: Set to `development` for local development

2. **Database**: The SQLite database (`instance/secure_notes.db`) is created automatically on first run. The schema is defined in `instance/schema.sql`.

### Accessing the Application

Once running, access the application at:
- **URL:** http://127.0.0.1:5000
- **Home Page:** http://127.0.0.1:5000/
- **Login:** http://127.0.0.1:5000/auth/login
- **Register:** http://127.0.0.1:5000/auth/register

---

## Usage Guidelines

### Getting Started

1. **Register a New Account**
   - Navigate to the Register page
   - Choose a username (3-20 characters)
   - Set a password (minimum 6 characters)
   - Click "Register" to create your account

2. **Login**
   - Enter your username and password
   - Click "Login" to access your notes dashboard
   - Note: Rate limiting applies (5 attempts per minute)

3. **Create a Note**
   - Click "Create Note" from the dashboard
   - Enter a title and content
   - Click "Create" to save

4. **View Notes**
   - All your notes appear on the dashboard
   - Click on a note title to view full details
   - **User Role:** See only your own notes
   - **Moderator/Admin Role:** See all notes in the system

5. **Edit a Note**
   - Click "Edit" on a note you own
   - Modify title or content
   - Click "Update" to save changes
   - **Note:** Users can only edit their own notes (admins can edit any)

6. **Delete a Note**
   - Click "Delete" on a note
   - Confirm deletion
   - **Note:** Users can only delete their own notes (moderators/admins can delete any)

7. **Admin Dashboard** (Admin role only)
   - Access via "Admin" link in navigation
   - View all users and notes in the system
   - Monitor system activity

### Important Notes

- **Session Security:** Sessions expire when you close the browser (or after inactivity)
- **Rate Limiting:** Login and registration are rate-limited to prevent brute force attacks
- **Ownership:** Notes are protected by ownership checks - you cannot access notes belonging to other users (unless you're a moderator/admin)
- **Audit Logging:** All security-relevant actions are logged in `logs/audit.log`

---

## Security Improvements

### Security Requirements (SR1-SR9) Implementation

| Requirement ID | Requirement | Status | Version | Percentage |
|---------------|-------------|--------|---------|------------|
| **SR1** | Password Hashing | ✅ Completed | v2.0.1 | 100% |
| **SR2** | CSRF Protection | ✅ Completed | v2.1.1 | 100% |
| **SR3** | Session Security | ✅ Completed | v2.0.2 | 100% |
| **SR4** | Input Sanitisation | ✅ Completed | v2.1.1, v2.3.3 | 100% |
| **SR5** | RBAC | ✅ Completed | v2.2.1 | 100% |
| **SR6** | Secure Headers | ✅ Completed | v2.3.1 | 100% |
| **SR7** | Rate Limiting | ✅ Completed | v2.3.1 | 100% |
| **SR8** | Audit Logging | ✅ Completed | v2.3.2 | 100% |
| **SR9** | Error Management | ✅ Completed | v2.3.2 | 100% |

### OWASP Top 10 2025 Coverage

| OWASP Category | Vulnerability | Status | Mitigation |
|---------------|---------------|--------|------------|
| **A01** | Broken Access Control | ✅ Mitigated | RBAC + ownership checks (v2.2.1) |
| **A02** | Security Misconfiguration | ✅ Mitigated | Flask-Talisman headers (v2.3.1) |
| **A04** | Cryptographic Failures | ✅ Mitigated | bcrypt password hashing (v2.0.1) |
| **A05** | Injection | ✅ Mitigated | Parameterized queries + CSRF (v2.3.3, v2.1.1) |
| **A07** | Authentication Failures | ✅ Mitigated | Flask-Login + rate limiting (v2.0.2, v2.3.1) |
| **A09** | Logging & Alerting Failures | ✅ Mitigated | Comprehensive audit logging (v2.3.2) |
| **A10** | Mishandling of Exceptional Conditions | ✅ Mitigated | Error logging + handlers (v2.3.2) |

### Key Security Features

1. **Parameterized Queries**: All SQL queries use `?` placeholders to prevent SQL injection
2. **Password Security**: bcrypt hashing with salt (no plaintext storage)
3. **CSRF Tokens**: All forms protected with Flask-WTF CSRF tokens
4. **Secure Sessions**: Flask-Login with HttpOnly, Secure, SameSite cookies
5. **Rate Limiting**: Login (5/min) and registration (3/min) limits
6. **Security Headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
7. **Input Validation**: WTForms validators on all user inputs
8. **RBAC**: Three-tier role system (User, Moderator, Admin)
9. **Audit Logging**: All auth and CRUD events logged with user context
10. **Error Handling**: Secure error messages with comprehensive logging

---

## Testing Process

### Static Application Security Testing (SAST)

#### Bandit Analysis

**Baseline (v1.4):**
- 11 Medium severity issues (all SQL injection)
- 0 High severity issues

**Final (v2.4):**
- ✅ 0 SQL injection issues (100% elimination)
- ✅ 0 Medium severity issues
- ✅ 0 High severity issues
- ⚠️ 2 Low severity issues (acceptable try-except-pass patterns)

**Reports:** `docs/evidence/bandit-v1.4-report.txt`, `docs/evidence/bandit-v2.4-report.txt`

#### Semgrep Analysis

**Baseline (v1.5):**
- 13 SQL injection findings (ERROR severity)
- All from string concatenation in SQL queries

**Final (v2.4):**
- ✅ 0 SQL injection vulnerabilities (100% elimination)
- ⚠️ 1 false positive (log message f-string, not SQL query)

**Reports:** `docs/evidence/semgrep-v1.5-report.json`, `docs/evidence/semgrep-v2.4-report.json`

**Comparison Report:** `docs/evidence/v2.4-comparison-report.md`

### Functional Testing

**Framework:** pytest with Flask-Testing

**Test Coverage:**
- Authentication routes (register, login, logout)
- Notes CRUD operations
- RBAC access control
- Admin dashboard access

**Test Files:**
- `tests/test_auth.py` - Authentication tests
- `tests/test_notes.py` - Notes CRUD tests
- `tests/test_admin.py` - Admin access tests

**Run Tests:**
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Security Feature Testing

1. **SQL Injection Prevention**
   - ✅ Tested with malicious input in all forms
   - ✅ Verified parameterized queries prevent injection
   - ✅ SAST tools confirm 0 SQL injection vulnerabilities

2. **CSRF Protection**
   - ✅ Verified CSRF tokens present on all forms
   - ✅ Tested POST requests without tokens (rejected)
   - ✅ Confirmed token validation working

3. **RBAC and Access Control**
   - ✅ Tested User role (own notes only)
   - ✅ Tested Moderator role (view all, edit own, delete any)
   - ✅ Tested Admin role (full access)
   - ✅ Verified 403 errors for unauthorized access

4. **Rate Limiting**
   - ✅ Tested login rate limit (5 attempts/minute)
   - ✅ Tested registration rate limit (3 attempts/minute)
   - ✅ Verified 429 errors when limit exceeded

5. **Password Security**
   - ✅ Verified bcrypt hashes in database
   - ✅ Confirmed no plaintext passwords stored
   - ✅ Tested password strength requirements

---

## Contributions and References

### Original Development

This project was developed from scratch as part of the Secure Web Development (H9SWD) module at National College of Ireland. The application follows a structured Secure Software Development Lifecycle (SSDLC) approach, evolving from an intentionally insecure baseline to a production-ready secure application.

### Technologies and Frameworks Used

- **Flask 3.0.0** - Web framework ([Flask Documentation](https://flask.palletsprojects.com/))
- **Flask-Login 0.6.3** - User session management ([Flask-Login Documentation](https://flask-login.readthedocs.io/))
- **Flask-WTF 1.2.1** - CSRF protection and form validation ([Flask-WTF Documentation](https://flask-wtf.readthedocs.io/))
- **Flask-Talisman 1.1.0** - Security headers ([Flask-Talisman Documentation](https://github.com/GoogleCloudPlatform/flask-talisman))
- **Flask-Limiter 3.5.0** - Rate limiting ([Flask-Limiter Documentation](https://flask-limiter.readthedocs.io/))
- **bcrypt 4.1.2** - Password hashing ([bcrypt Documentation](https://github.com/pyca/bcrypt/))
- **WTForms 3.1.2** - Form validation ([WTForms Documentation](https://wtforms.readthedocs.io/))
- **SQLite** - Database (Python standard library)
- **Bandit** - Static security analysis ([Bandit Documentation](https://bandit.readthedocs.io/))
- **Semgrep** - SAST tool with OWASP rules ([Semgrep Documentation](https://semgrep.dev/docs/))
- **pytest** - Testing framework ([pytest Documentation](https://docs.pytest.org/))

### Security Standards and Guidelines

- **OWASP Top 10 2025** - Application Security Risks ([OWASP Top 10](https://owasp.org/www-project-top-ten/))
- **OWASP ASVS** - Application Security Verification Standard ([OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/))
- **CWE Top 25** - Common Weakness Enumeration ([CWE Top 25](https://cwe.mitre.org/top25/))

### References

1. Flask Project. (2024). *Flask Documentation*. Retrieved from https://flask.palletsprojects.com/
2. OWASP Foundation. (2025). *OWASP Top 10 - 2025*. Retrieved from https://owasp.org/www-project-top-ten/
3. Python Software Foundation. (2024). *Python Documentation*. Retrieved from https://docs.python.org/3/
4. Semgrep, Inc. (2024). *Semgrep Documentation*. Retrieved from https://semgrep.dev/docs/
5. PyCQA. (2024). *Bandit - A security linter for Python code*. Retrieved from https://bandit.readthedocs.io/

---

## Version History

| Version | Description | Key Features |
|---------|-------------|--------------|
| **v0.0** | Repository initialization | Project setup, PRD, dev plan |
| **v0.1** | Flask scaffold | App factory, configuration |
| **v0.2** | Blueprint structure | Auth, notes, admin blueprints |
| **v0.3.1-0.3.5** | Frontend scaffolding | Templates, CSS, UI structure |
| **v0.4-0.5** | Database setup | SQLite schema, middleware |
| **v0.9.1-0.9.4** | Functional baseline | CRUD operations, intentionally insecure |
| **v1.0-1.3** | Insecure MVP | All vulnerabilities demonstrated |
| **v1.4-1.5.1** | Testing phase | Bandit, Semgrep, pytest |
| **v2.0.1** | Password hashing | bcrypt implementation |
| **v2.0.2** | Session security | Flask-Login integration |
| **v2.1.1** | CSRF & validation | Flask-WTF, input sanitization |
| **v2.2.1** | RBAC | Role-based access control |
| **v2.3.1** | Security headers | Flask-Talisman, rate limiting |
| **v2.3.2** | Audit logging | Comprehensive event logging |
| **v2.3.3** | SQL injection fix | Parameterized queries |
| **v2.4** | Verification | Final SAST re-run, comparison |
| **v2.5** | Documentation | README, UI improvements |

---

## License

This project is developed for educational purposes as part of the Secure Web Development (H9SWD) module at National College of Ireland.

---

## Author

**Konstanty Litwinow**  
MSc Cybersecurity, National College of Ireland  
**Student ID:** 23437073  
**GitHub:** [https://github.com/Kostek02](https://github.com/Kostek02)  
**Email:** x23437073@student.ncirl.ie

---

**Last Updated:** v2.5 - Documentation and UI Improvements  
**Status:** ✅ Production-Ready - All Security Requirements Complete
