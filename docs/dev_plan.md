# Secure Notes Web Application – Development Plan

**Author:** Konstanty Litwinow  
**Programme:** MSc Cybersecurity (National College of Ireland)  
**Module:** Secure Web Development (H9SWD)  
**Assessment:** CA2 – Secure Web Application  
**Framework:** Flask (Python 3.12)  
**Repository:** [https://github.com/Kostek02/CA2](https://github.com/Kostek02/CA2)

---

## 1. Overview

This development plan defines the structured, secure, and traceable approach used to build the **Secure Notes Web Application**.  
The project follows a practical **Secure Software Development Lifecycle (SSDLC)**, evolving from an intentionally insecure baseline to a hardened, production-ready system.

All development, documentation, and version control are performed through Git using a transparent, multi-phase workflow supported by meaningful commit messages, evidence screenshots, and version tags.

---

## 2. Development Methodology

The project applies an **iterative and incremental** SSDLC process with continuous feedback and validation:

1. **Planning & Requirements Definition** – establish system and security requirements (see `prd.md`).
2. **Design & Scaffold** – create Flask foundation, configuration, and environment scripts.
3. **Implementation** – develop functional and insecure builds.
4. **Testing & Analysis** – perform static/dynamic analysis with Bandit, Semgrep, and pytest.
5. **Hardening & Refactor** – mitigate vulnerabilities using secure design principles and Flask libraries.
6. **Verification & Documentation** – validate controls, record evidence, and finalise deliverables.

Each iteration strengthens both code functionality and security posture.

---

## 3. Branching Strategy

| Branch | Purpose |
|--------|----------|
| **main** | Stable branch containing only verified and tagged releases (v0.0 → v2.6). |
| **dev** | Active development branch used for all implementation, testing, and incremental commits. |

Both are mirrored remotely as **origin/main** and **origin/dev** on GitHub to provide full visibility.

**Workflow Summary**
1. Development occurs exclusively in `dev`.  
2. Milestone completion triggers a merge into `main`.  
3. Each merge includes a tag (e.g., `v0.1-setup`, `v1.0-insecure`, `v2.0-secure`).  
4. Internal evidence and environment files remain excluded via `.gitignore`.

This approach ensures clear traceability and meets CA2’s requirement for **visible progressive commit history**.

---

## 4. Development Phases and Deliverables

| Phase | Version Tag | Description | Key Deliverables |
|-------|--------------|-------------|------------------|
| **Phase 0 – Initialisation** | `v0.0-prd` | Repository structure, environment setup, config files, and internal docs. | `.env`, `requirements.txt`, `config.py`, `prd.md`, `dev_plan.md` |
| **Phase 1 – Flask Scaffold** | `v0.1-setup` | Implement app factory, base route, run scripts (`run_app.sh` / `run_app.ps1`). | Flask app factory (`app/__init__.py`), `run.py`, run scripts, working root route |
| **Phase 2 – Blueprint Structure** | `v0.2-blueprints` | Add `auth`, `notes`, and `admin` blueprints with placeholder routes. | `app/auth/routes.py`, `app/notes/routes.py`, `app/admin/routes.py`, registered blueprints |
| **Phase 2.1 – Frontend Scaffolding** | `v0.3-home` | Add base templates & static assets (Jinja `base.html`, `home.html`, CSS) and simple nav. | `templates/base.html`, `templates/home.html`, `static/css/style.css`, screenshot of rendered home |
| **Phase 2.2 – Database Scaffolding** | `v0.4-db` | Introduce local persistence (SQLite schema) and a simple DB connection helper (insecure by design for now). | `instance/schema.sql` or migrations, `app/db.py` helper, DB creation screenshot |
| **Phase 2.3 – App Helpers & Middleware** | `v0.5-middleware` | Add common app helpers (flash, context processors), basic error handlers (403/404/500 placeholders) and simple middleware hooks. | `app/helpers.py`, `app/error_handlers.py`, `templates/403.html`, `templates/404.html`, evidence screenshot |
| **Phase 3 – Insecure MVP (Intentional Vulnerabilities)** | `v1.0–v1.3` | Deliberately implement the insecure baseline to demonstrate vulnerabilities and form the testing target for hardening. | Demoable insecure app (auth + notes + admin) for testing and exploitation evidence |
| • `v1.0-insecure-auth` | `v1.0-insecure-auth` | Implement `/register`, `/login`, `/logout` using raw SQL and plaintext password storage (intentional). | Auth routes, raw SQL usage, evidence of login flow + SQLi PoC screenshot |
| • `v1.1-insecure-crud` | `v1.1-insecure-crud` | Implement `/notes` CRUD without ownership checks (IDOR) and without input sanitisation (stores arbitrary HTML). | Notes CRUD routes, sample stored XSS demonstration screenshot |
| • `v1.2-insecure-admin` | `v1.2-insecure-admin` | Admin dashboard accessible to all users (no RBAC), exposing user lists and notes. | Admin routes, evidence of unprotected admin access |
| • `v1.3-full-insecure` | `v1.3-full-insecure` | Combine the above into a working insecure MVP used as the baseline for security testing. | Full insecure app, consolidated exploitation screenshots (SQLi, XSS, IDOR) |
| **Phase 4 – Testing & Analysis** | `v1.4–v1.5` | Run static and dynamic analysis to create a vulnerability baseline (Bandit, Semgrep, pytest). | `docs/evidence/` results for Bandit and Semgrep, `tests/` pytest outputs, vulnerability table |
| **Phase 5 – Security Refactor** | `v2.0–v2.3` | Apply secure design and fixes mapped to SR1–SR9 and OWASP Top 10 (2025). Work is split into taggable steps for clear before/after evidence. | Hardened implementations and tests showing mitigation of each vulnerability |
| • `v2.0-auth-hardening` | `v2.0-auth-hardening` | Replace plaintext passwords with bcrypt, integrate Flask-Login, and strengthen session handling. | Bcrypt integration, Flask-Login setup, tests verifying hashed passwords |
| • `v2.1-validation-csrf` | `v2.1-validation-csrf` | Add Flask-WTF forms, CSRF protection, and input validation/sanitisation. | CSRF tokens on forms and sanitisation evidence |
| • `v2.2-rbac-protection` | `v2.2-rbac-protection` | Enforce RBAC (User/Moderator/Admin) and per-record ownership checks to prevent IDOR. | RBAC decorators, ownership checks, tests demonstrating 403 on unauthorized access |
| • `v2.3-secure-headers` | `v2.3-secure-headers` | Apply Flask-Talisman for CSP/HSTS and Flask-Limiter for rate limiting; disable debug in production config. | CSP/HSTS headers screenshot, rate limiting configured |
| **Phase 6 – Verification & Documentation (Final Release)** | `v2.4–v2.6` | Final verification, test re-run, SAST comparison, evidence compilation, and report/video production. | Final tests, Bandit/Semgrep diffs, final README, technical report, unlisted demo video link |

---

## 5. Secure Coding and Testing Approach

### 5.1 Static Analysis
| Tool | Purpose |
|------|---------|
| **Bandit** | Detects common Python security issues (e.g., unsafe functions, weak cryptography). |
| **Semgrep** | Applies OWASP Top 10 rule sets to identify framework-level weaknesses. |
| **Flake8** | Enforces PEP 8 compliance and code quality. |

### 5.2 Dynamic & Functional Testing
| Tool | Purpose |
|------|---------|
| **pytest** | Automates route, authentication, and CRUD verification. |
| **Manual testing** | Confirms runtime behaviour of mitigations (CSRF tokens, secure cookies, access control). |

### 5.3 Security Verification
Validation checkpoints include:
- Presence of CSRF tokens in all forms.  
- Passwords hashed using bcrypt (verified in database).  
- Secure headers (`CSP`, `HSTS`, `X-Frame-Options`) visible in browser inspector.  
- IDOR/SQLi attempts correctly denied with `403 Forbidden`.  

---

## 6. Documentation and Evidence Management

All documentation resides under `/docs/` and `/docs/evidence/`.

| Artifact | Description |
|-----------|-------------|
| **prd.md** | Defines functional and security requirements. |
| **dev_plan.md** | Defines project roadmap and branching model. |
| **/docs/evidence/** | Screenshots, Bandit/Semgrep outputs, pytest logs, version proofs. |
| **README.md** | High-level overview for public repository. |
| **Internal Notes** | Non-public drafts and internal planning materials (excluded from repo). |

Evidence is collected after each tagged milestone to provide a chronological proof of progress and security improvement.

---

## 7. OWASP 2025 Integration

Each refactor phase (v2.0–v2.3) directly addresses **OWASP Top 10 (2025)** categories:

| OWASP Category | Implemented Controls |
|----------------|----------------------|
| **A01 – Broken Access Control** | RBAC, per-record ownership validation. |
| **A02 – Security Misconfiguration** | `.env`-based configuration, Flask-Talisman, disabled debug mode. |
| **A04 – Cryptographic Failures** | bcrypt password hashing, secure session cookies. |
| **A05 – Injection** | Parameterised queries, sanitised templates. |
| **A07 – Authentication Failures** | Flask-Login session management and validation. |
| **A09 – Logging & Alerting Failures** | Audit logging of authentication and CRUD actions. |
| **A10 – Mishandling of Exceptional Conditions** | Custom error handlers for 403/404/500 responses. |

---

## 8. Success Metrics

1. **Security Compliance** – all SR1–SR9 requirements verified.  
2. **Functional Completeness** – FR1–FR7 successfully implemented.  
3. **Testing Coverage** – pytest ≥ 80% route coverage.  
4. **Auditability** – consistent commit history and tagging.  
5. **Quality Assurance** – zero high-severity Bandit/Semgrep findings by final release.

---

## 9. References

- OWASP Foundation (2025) *OWASP Top 10: 2025 – The Ten Most Critical Web Application Security Risks.* Available at: <https://owasp.org/Top10/> (Accessed: November 2025)  
- *Flask Documentation – Security Best Practices*  
- *Python 3.12 Official Docs*  
- NCI Secure Web Development (H9SWD) CA2 Brief  
- *Bandit* and *Semgrep* tool guides  

---

*This document defines the development strategy, branch workflow, and verification model for the Secure Notes Web Application, complementing the `prd.md` as part of NCI MSc Cybersecurity – H9SWD CA2.*

---

**End of Document**