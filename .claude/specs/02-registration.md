# Spec: Registration

## Overview
Implement user registration so new visitors can create a Spendly account.
This step adds the `POST /register` route that validates form input, hashes
the password, inserts a new user row, and redirects to the login page on
success. The `GET /register` route and the `register.html` template already
exist; this step wires in the form handler and error feedback.

## Depends on
- Step 01 — Database Setup (`get_db`, `users` table, werkzeug available)

## Routes
- `POST /register` — process registration form — public

## Database changes
No new tables or columns. Requires two new helpers in `database/db.py`:
- `get_user_by_email(email)` — returns a user row or `None`
- `create_user(name, email, password_hash)` — inserts a new user row

## Templates
- **Modify:** `templates/register.html` — add the HTML form (name, email,
  password, confirm password fields) and a block to display validation errors

## Files to change
- `app.py` — add `POST /register` route; add `app.secret_key`; import
  `redirect`, `request`, `flash`, `get_flashed_messages`, `session`,
  `url_for` from flask; import `generate_password_hash` from werkzeug
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — add form markup and error display

## Files to create
None

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterized queries only (`?` placeholders — never f-strings in SQL)
- Passwords hashed with `werkzeug.security.generate_password_hash` before
  storing; never store plaintext
- Use CSS variables — never hardcode hex values in templates or stylesheets
- All templates extend `base.html`
- `app.secret_key` must be set before flash messages work; use a hard-coded
  dev string for now (e.g. `"dev-secret-change-me"`) — a future step will
  move it to config
- Validate in this order and show the first error that applies:
  1. All fields required (name, email, password, confirm password)
  2. Email already registered
  3. Password and confirm password must match
  4. Password must be at least 8 characters
- Use `flask.flash()` for error messages; render them at the top of the form
- On success: redirect to `url_for('login')` — do NOT log the user in here
  (that is Step 3)
- `abort(405)` is not needed — Flask returns 405 automatically for
  unregistered methods

## Definition of done
- [ ] Submitting the form with all valid fields creates a new user in the DB
      and redirects to `/login`
- [ ] Submitting with an email already in the DB shows an error message on
      the register page without creating a duplicate row
- [ ] Submitting with mismatched passwords shows an error message
- [ ] Submitting with a password shorter than 8 characters shows an error
- [ ] Submitting with any blank field shows an error
- [ ] The demo user (`demo@spendly.com`) can still log in via the seeded row
      (no regressions to existing data)
- [ ] Visiting `GET /register` still renders the empty form
