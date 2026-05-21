# Spec: Login and Logout

## Overview
Implement credential-based login and session-backed logout so registered users
can authenticate and access protected areas of Spendly. This step converts the
existing stub `GET /login` route into a full `GET + POST` handler that validates
email/password against the stored hash, writes `user_id` into Flask's signed
cookie session on success, and redirects to the profile page. The `GET /logout`
stub is replaced with a handler that clears the session and redirects to the
landing page. The shared nav in `base.html` is updated to show context-aware
links (Sign in / Get started when logged out; Sign out when logged in).

## Depends on
- Step 01 — Database Setup (`get_db`, `users` table, werkzeug available)
- Step 02 — Registration (`get_user_by_email`, `password_hash` column populated)

## Routes
- `GET  /login`  — render login form — public
- `POST /login`  — validate credentials, set session, redirect — public
- `GET  /logout` — clear session, redirect to landing — public (safe to call when already logged out)

## Database changes
No new tables or columns.

New helper required in `database/db.py`:
- `get_user_by_id(user_id)` — returns the user row for the given id, or `None`
  (needed by `base.html` to display the logged-in user's name in the nav)

## Templates
- **Modify:** `templates/login.html`
  - Replace `{% if error %}{{ error }}{% endif %}` block with `get_flashed_messages()` loop (align with registration pattern)
  - Change hardcoded `action="/login"` to `action="{{ url_for('login') }}"`
  - Pre-fill `value="{{ request.form.email }}"` on the email field so the user does not have to retype on error
- **Modify:** `templates/base.html`
  - Import nothing — Jinja2 can read `session` directly
  - Replace the static nav links block with a conditional:
    - Logged out (`session` has no `user_id`): show "Sign in" + "Get started"
    - Logged in: show the user's name (loaded via `get_user_by_id`) and a "Sign out" link pointing to `url_for('logout')`

## Files to change
- `app.py`
  - Add `session` and `check_password_hash` to imports
  - Add `get_user_by_id` to the `database.db` import line
  - Convert `login()` to accept `methods=["GET", "POST"]`; add POST handler logic
  - Replace the `logout()` stub body with `session.clear()` + redirect
- `database/db.py`
  - Add `get_user_by_id(user_id)` helper
- `templates/login.html`
  - Switch error display to flash; fix action URL; add email pre-fill
- `templates/base.html`
  - Add conditional nav block based on `session.get('user_id')`

## Files to create
None

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already
available via the existing werkzeug install.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (`?` placeholders — never f-strings in SQL)
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values in templates or stylesheets
- All templates extend `base.html`
- Use `flask.flash()` for login error messages and display them with
  `get_flashed_messages()` — do NOT pass an `error=` variable to `render_template`
- Login POST validation order:
  1. Both fields required (email + password)
  2. No account found for that email → generic message ("Invalid email or password")
  3. Password hash does not match → same generic message (never reveal which field is wrong)
- On successful login: `session['user_id'] = user.id`, then `redirect(url_for('profile'))`
- On failed login: `flash(...)`, then `return render_template("login.html")` (do NOT redirect on error)
- Logout must call `session.clear()` (not `session.pop`), then `redirect(url_for('landing'))`
- `base.html` nav: call `get_user_by_id(session['user_id'])` only when `session.get('user_id')` is truthy — guard against missing/stale session keys
- Do NOT implement access control / `@login_required` in this step — that is a later concern

## Definition of done
- [ ] `POST /login` with valid credentials sets the session and redirects to `/profile`
- [ ] `POST /login` with an unregistered email shows "Invalid email or password" on the login page
- [ ] `POST /login` with a wrong password shows "Invalid email or password" on the login page
- [ ] `POST /login` with either field blank shows a validation error
- [ ] After login the nav shows the user's name and a "Sign out" link instead of "Sign in / Get started"
- [ ] Clicking "Sign out" clears the session and redirects to the landing page
- [ ] After logout the nav reverts to "Sign in / Get started"
- [ ] Visiting `/login` while already logged in still renders the form (no forced redirect — that is a later step)
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in and out successfully
- [ ] Registration flow still works and redirects to `/login` (no regressions)
