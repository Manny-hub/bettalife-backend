# BettaLife Backend - Django REST API

Nigerian Food Recommendation System API

## Features
- 🍲 100+ Nigerian foods database
- 🎯 AI-powered meal recommendations
- 📊 Nutritional tracking
- 💰 Budget-friendly meal planning
- ❤️ Health condition support (diabetes, hypertension)

## Tech Stack
- Django 4.2.7
- Django REST Framework
- PostgreSQL/SQLite
- Python 3.8+

## Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/bettalife-backend.git
cd bettalife-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed database
python manage.py seed_data

# Run server
python manage.py runserver
```

## API Endpoints

- `/api/recipes/` - Browse recipes
- `/api/meal-plans/generate/` - Generate meal plan
- `/api/recommendations/` - Get personalized recommendations
- `/api/health-tips/` - Health & nutrition tips

## Documentation

API docs available at: `http://localhost:8000/swagger/`

## License

MIT
