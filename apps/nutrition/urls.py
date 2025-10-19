# urls.py - API URL Configuration

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    FoodViewSet,
    RecipeViewSet,
    MealPlanViewSet,
    MealLogViewSet,
    RecommendationViewSet,
    HealthTipViewSet
)

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'foods', FoodViewSet, basename='food')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'meal-plans', MealPlanViewSet, basename='mealplan')
router.register(r'meal-logs', MealLogViewSet, basename='meallog')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')
router.register(r'health-tips', HealthTipViewSet, basename='healthtip')

urlpatterns = [
    path('', include(router.urls)),
]


# Example API Endpoints Available:

"""
USER PROFILE:
GET    /api/profile/me/                 - Get current user profile
PUT    /api/profile/update_profile/     - Update user profile

FOODS:
GET    /api/foods/                       - List all foods
GET    /api/foods/{id}/                  - Get food details
GET    /api/foods/categories/            - List food categories
GET    /api/foods/seasonal/              - Get seasonal foods
GET    /api/foods/?category=Proteins     - Filter by category
GET    /api/foods/?vegetarian=true       - Filter vegetarian foods
GET    /api/foods/?search=rice           - Search foods

RECIPES:
GET    /api/recipes/                     - List all recipes
GET    /api/recipes/{id}/                - Get recipe details with ingredients
GET    /api/recipes/popular/             - Get popular recipes
GET    /api/recipes/quick/               - Get quick recipes (< 30 min)
GET    /api/recipes/budget_friendly/     - Get affordable recipes
GET    /api/recipes/?meal_type=breakfast - Filter by meal type
GET    /api/recipes/?difficulty=easy     - Filter by difficulty
GET    /api/recipes/?max_cost=1000       - Filter by max cost
POST   /api/recipes/{id}/rate/           - Rate a recipe

MEAL PLANS:
GET    /api/meal-plans/                  - List user's meal plans
GET    /api/meal-plans/today/            - Get today's meal plan
GET    /api/meal-plans/week/             - Get this week's meal plans
POST   /api/meal-plans/generate/         - Generate AI meal plan
POST   /api/meal-plans/{id}/mark_followed/ - Mark plan as followed
POST   /api/meal-plans/                  - Create custom meal plan
PUT    /api/meal-plans/{id}/             - Update meal plan

MEAL LOGS:
GET    /api/meal-logs/                   - List meal logs
GET    /api/meal-logs/today/             - Get today's logs
GET    /api/meal-logs/stats/?days=7      - Get logging statistics
POST   /api/meal-logs/                   - Log a meal
DELETE /api/meal-logs/{id}/              - Delete a log

RECOMMENDATIONS:
GET    /api/recommendations/for_you/?meal_type=lunch  - Personalized recommendations
GET    /api/recommendations/seasonal/                  - Seasonal recommendations
GET    /api/recommendations/grocery_list/?days=7       - Generate grocery list
GET    /api/recommendations/nutritional_gaps/          - Analyze nutritional gaps

HEALTH TIPS:
GET    /api/health-tips/                 - List health tips
GET    /api/health-tips/daily_tip/       - Get random daily tip
GET    /api/health-tips/{id}/            - Get specific tip
"""