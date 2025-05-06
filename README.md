# Interview Review Discussion Platform

A web platform built with Django that allows users to share and discuss their interview experiences. This platform aims to help job seekers by providing a space where they can learn from others' interview experiences and prepare better for their own interviews.

## Features

- Share interview experiences
- Comment and discuss on interview reviews
- User authentication (Sign up, Sign in, Logout)
- Favorite interviews to collect
- Flash messages for user feedback
- Responsive design with Tailwind CSS and DaisyUI
- Dynamic interactions using HTMX and Alpine.js

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, Tailwind CSS, DaisyUI
- **Database**: SQLite3
- **Template Engine**: Django Templates
- **Dynamic Interactions**: HTMX, Alpine.js

## Project Structure

```
.
├── interviews/            
│   ├── templates/         
│   ├── views.py           
│   ├── models.py          
│   ├── forms.py           
│   ├── urls.py            
│   └── migrations/        
├── pages/                 
│   ├── templates/         
│   ├── views.py           
│   ├── urls.py            
│   └── migrations/        
├── users/                 
│   ├── templates/         
│   ├── views.py           
│   ├── forms.py           
│   ├── urls.py            
│   └── migrations/        
├── templates/             
│   ├── layouts/           
│   ├── shared/            
├── my_project/            
│   ├── settings.py        
│   ├── urls.py            
│   ├── asgi.py            
│   └── wsgi.py            
├── manage.py              
├── requirements.txt       
├── db.sqlite3             
└── Makefile               
```

## Getting Started

1. Clone the repository:
   ```
   git clone <repository-url>
   cd 0411_project_interview_review
   ```
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
6. Access the application at:
   ```
   http://127.0.0.1:8000/
   ```

## Notes

- Ensure Python 3.13 or higher is installed.
- Use the `Makefile` for common commands:
  ```
  make runserver
  make makemigrations
  make migrate
  ```
