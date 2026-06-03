# Berachaiah Abolaji — Portfolio (Django)

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Create your admin user (or use the seeded one)
python manage.py createsuperuser

# 4. Seed default content (optional — only needed on fresh DB)
python manage.py shell < seed.py

# 5. Run the dev server
python manage.py runserver
```

Then visit:
- **Portfolio:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin-panel/login/
  - Default login: `admin` / `admin123` (change this immediately!)

## Admin Panel Features
| Section | What you can do |
|---|---|
| **Site Settings** | Edit hero headline, about text, upload portrait |
| **Hero Images** | Upload carousel photos, set order & captions |
| **Projects** | Add/edit/delete projects with images, tags, status |
| **Research** | Manage research items |
| **Certificates** | Add/remove certifications |
| **Tech Stack** | Manage stack categories and items |
| **Messages** | View all contact form submissions |

## Deployment

### cPanel / Passenger WSGI
1. Upload this folder to your hosting
2. Set `DEBUG = False` and `ALLOWED_HOSTS = ['yourdomain.com']` in `settings.py`
3. Set `SECRET_KEY` to a real random secret
4. Run `python manage.py collectstatic`
5. Point Passenger to `portfolio/wsgi.py`

### Railway / Render
1. Push to GitHub
2. Add `gunicorn` to requirements.txt
3. Set `Procfile`: `web: gunicorn portfolio.wsgi`
4. Set environment variables for `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`

## Changing Admin Password
```bash
python manage.py changepassword admin
```
