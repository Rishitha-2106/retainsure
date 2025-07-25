# CHANGES.md

## Major Issues Identified

1. **Security Flaws**
   - Passwords were stored in plaintext.
   - No input validation (email format, missing fields, etc.).
   - SQL Injection risk due to unsafe queries.

2. **Poor Code Structure**
   - No reuse of DB connection logic.
   - Repeated logic in multiple places.
   - No meaningful error messages or HTTP status codes.

3. **Lack of Best Practices**
   - No use of HTTP status codes consistently.
   - No password hashing.
   - Missing email format validation.

---

## Changes Made

### 1. Security Improvements
- Used `werkzeug.security` to hash passwords securely.
- Added validation for email format using regex.
- Validated required fields in all relevant routes.
- Used parameterized queries to prevent SQL injection.

### 2. Code Quality & Maintainability
- Reused `get_db_connection()` across all routes.
- Replaced raw queries with parameterized ones.
- Extracted `validate_user_data()` to clean up POST/PUT code.
- Returned appropriate HTTP status codes (`200`, `201`, `400`, `404`, `409`, `401`).

### 3. Error Handling
- Clear messages for each failure scenario (e.g., missing fields, invalid email, existing email).
- Used `try-except` for database insert to catch uniqueness constraint errors.

---

## Assumptions / Trade-offs

- Still kept everything inside `app.py` as per instructions, which sacrifices ideal modularity.
- No session/token-based auth added due to constraint of not adding new features.

---

## If I Had More Time

- Split code into modules (`routes/`, `services/`, `models/`, etc.).
- Add unit and integration tests with `pytest` and `Flask-Testing`.
- Implement token-based auth (e.g., JWT).
- Migrate from SQLite to PostgreSQL for better scalability.
- Add API schema validation using `pydantic` or `marshmallow`.

---

## AI Usage Disclosure

- **Tools Used:** ChatGPT
- **Used For:**
  - Refactoring strategy
  - Regex for email validation
  - HTTP status code guidelines
- **All code reviewed and modified manually to fit requirements**
