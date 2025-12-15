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
| **Phase 0 – Initialisation** | `v0.0-prd` | Repository structure, environment setup, config files, and internal documentation. | `.env`, `requirements.txt`, `config.py`, `prd.md`, `dev_plan.md` |
| **Phase 1 – Flask Scaffold** | `v0.1-setup` | Implement Flask app factory, base route, and run scripts (`run_app.sh` / `run_app.ps1`). | `app/__init__.py`, `run.py`, run scripts, verified local app execution |
| **Phase 2 – Blueprint Structure** | `v0.2-blueprints` | Add `auth`, `notes`, and `admin` blueprints with placeholder routes for modular architecture. | `app/auth/routes.py`, `app/notes/routes.py`, `app/admin/routes.py`, registered blueprints |
| **Phase 2.1 – Frontend Scaffolding** | `v0.3-home` → `v0.3.5` | Establish base templates, static assets, and initial UI placeholders. | `templates/base.html`, `templates/home.html`, `static/css/main.css`, homepage screenshot |
|  • `v0.3.1-Home` | — | Base and homepage rendering with global navigation. | `/home` route rendered, CSS verified |
|  • `v0.3.2-Auth Templates` | — | Add login + register pages via Jinja templates. | `/auth/login`, `/auth/register` |
|  • `v0.3.3-Notes Templates` | — | Add CRUD placeholders for note management. | `/notes`, `/notes/create`, `/notes/edit`, `/notes/view` |
|  • `v0.3.4-Admin Template` | — | Basic admin dashboard placeholder. | `/admin` rendered |
|  • `v0.3.5-UI Polish` | — | Refine CSS / layout before DB integration. | Updated `main.css`, screenshot |
| **Phase 2.2 – Database Scaffolding** | `v0.4-db` | Introduce SQLite schema + helper (intentionally insecure baseline). | `instance/schema.sql`, `app/db.py`, DB creation screenshot |
| **Phase 2.3 – App Helpers & Middleware** | `v0.5-middleware` | Add flash messages, context processors, error handlers (403/404/500), and middleware hooks. | `app/helpers.py`, `app/error_handlers.py`, `templates/403.html`, `templates/404.html`, evidence screenshot |

### Phase 2.4 – Functional Baseline (`v0.9.x`)
Establish a complete **working application** with intentional vulnerabilities.

| Sub-Phase | Version Tag | Description | Key Deliverables |
|------------|--------------|-------------|------------------|
| **Functional /Notes/** | `v0.9.1-notes-crud` | Implement full CRUD operations backed by SQLite. | Create/Edit/View/Delete notes, DB persistence proof |
| **Functional /Auth/** | `v0.9.2-auth-basic` | Add working `/register` and `/login` routes using raw SQL + plaintext storage. | Successful registration + login, DB user records |
| **Functional /Admin/** | `v0.9.3-admin-linkage` | Connect user–note relationships and basic admin overview (list users/notes). | `/admin` shows all records, privilege structure ready |
| **Functional Integration Tests** | `v0.9.4-stable-baseline` | Verify all routes + templates work end-to-end. Document all intentional vulnerabilities. | Full CRUD + Auth + Admin flow demo, evidence screenshots |

---

### Phase 3 – Insecure MVP (Intentional Vulnerabilities)
**Note:** All vulnerabilities were present in the functional baseline (v0.9.x) and verified during v0.9.4 testing. The insecure MVP consolidates these demonstrated vulnerabilities.

| Sub-Phase | Version Tag | Description | Key Deliverables |
|------------|--------------|-------------|------------------|
| **Insecure /Auth/** | `v1.0-insecure-auth` | Raw SQL auth with plaintext passwords → SQLi exploitation. | SQLi bypass screenshot, DB leak evidence |
| **Insecure /Notes/** | `v1.1-insecure-crud` | Missing ownership checks (IDOR) + unsanitised inputs (XSS). | Stored XSS + IDOR PoC evidence |
| **Insecure /Admin/** | `v1.2-insecure-admin` | No RBAC → unauthenticated access to admin routes. | Proof of unauthorised access |
| **Merged Insecure MVP** | `v1.3-full-insecure` | Consolidate all vulnerabilities into one testable application. All vulnerabilities demonstrated and documented in v0.9.4 testing. | Combined SQLi/XSS/IDOR exploitation screenshots, full vulnerability documentation |

---

### Phase 4 – Testing & Analysis
Conduct security scans and tests to create a baseline for later comparison.

| Sub-Phase | Version Tag | Description | Key Deliverables |
|------------|--------------|-------------|------------------|
| **Static Analysis – Bandit** | `v1.4-bandit` | Run Bandit on insecure code base. | Bandit report (`.txt / .html`) |
| **Static Analysis – Semgrep** | `v1.5-semgrep` | Apply OWASP rule sets to find flaws. | Semgrep report + vulnerability table |
| **Functional Testing – pytest** | `v1.5.1-tests` | Validate route responses and error codes. | pytest results log |

---

### Phase 5 – Security Refactor (`v2.0–v2.3`)
Incrementally secure the application and map mitigations to SR1–SR9 and OWASP 2025.

| Sub-Phase | Version Tag | Description | Key Deliverables |
|------------|--------------|-------------|------------------|
| **Auth Hardening** | `v2.0.1-bcrypt` | Introduce bcrypt hashing + secure password storage. | Verified hashes in DB |
|  • `v2.0.2-flask-login` | — | Add Flask-Login sessions + secure cookies. | Session validation evidence |
| **Validation & CSRF Protection** | `v2.1.1-csrf-forms` | Use Flask-WTF with CSRF tokens and input sanitisation. | Token presence + form validation screenshots |
| **RBAC & Ownership Protection** | `v2.2.1-role-checks` | Add RBAC decorators and record ownership validation. | 403 access tests per role |
| **Secure Headers & Rate Limiting** | `v2.3.1-talisman` | Apply Flask-Talisman (CSP/HSTS) and Flask-Limiter. | Response headers + rate-limit logs |
| **Audit Logging & Monitoring** | `v2.3.2-audit-logs` | Record auth/CRUD actions for visibility. | Log evidence files (`/logs/`) |

---

### Phase 6 – Verification & Documentation (Final Release)
Final validation, reporting, and demo submission.

| Sub-Phase | Version Tag | Description | Key Deliverables |
|------------|--------------|-------------|------------------|
| **Final SAST Re-run** | `v2.4-verification` | Re-run Bandit & Semgrep on hardened code. | Comparison report (`before vs after`) |
| **Documentation Update** | `v2.5-docs` | Update README, evidence tables, and final CA2 report. | Completed project docs |
| **Demonstration Video** | `v2.6-demo` | Record and upload demo walkthrough. | Link to video + screenshots |

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