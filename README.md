# Interview Review Discussion Platform

A web platform built with Django that allows users to share and discuss their interview experiences. This platform aims to help job seekers by providing a space where they can learn from others' interview experiences and prepare better for their own interviews.

## Features

- Share interview experiences
- Browse interview reviews by company
- Comment and discuss on interview reviews

## Tech Stack

- **Backend**: Django 5.2
- **Frontend**: HTML
- **Database**: SQLite3
- **Template Engine**: Django Templates

## Project Structure

```
.
├── interviews/            # Interview review application
│   ├── templates/        # HTML templates
│   ├── views.py         # View controllers
│   ├── models.py        # Database models
│   └── urls.py          # URL routing
├── pages/                # Static pages application
│   ├── templates/       # HTML templates
│   ├── views.py        # View controllers
│   └── urls.py         # URL routing
├── my_project/          # Project settings
│   ├── settings.py     # Django settings
│   └── urls.py         # Main URL routing
├── manage.py            # Django management script
├── requirements.txt     # Project dependencies
└── db.sqlite3          # SQLite database
```

## Getting Started

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```
