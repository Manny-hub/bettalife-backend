# recommendation_engine.py - AI-powered meal recommendation system

from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Q, Avg
import random


class MealRecommendationEngine:
    """
    Recommends meals based on user profile, health goals, budget, and nutritional needs.
    Uses a scoring system to rank recipes.
    """
    
    def __init__(self, user):
        self.user = user
        self.daily_calories = user.calculate_daily_calories()
        self.daily_budget = float(user.daily_budget) if user.daily_budget else 3000.0 # Default 3000 Naira
        
    def generate_daily_meal_plan(self, target_date=None):
        """
        Generate a complete meal plan for a day.
        Returns: dict with breakfast, lunch, dinner, and snack recommendations
        """
        if not target_date:
            target_date = date.today()
        
        # Calorie distribution (rough guideline)
        breakfast_calories = float(self.daily_calories) * 0.25
        lunch_calories = float(self.daily_calories) * 0.35
        dinner_calories = float(self.daily_calories) * 0.30
        snack_calories = float(self.daily_calories) * 0.10
        
        # Budget distribution
        breakfast_budget = float(self.daily_budget) * 0.25
        lunch_budget = float(self.daily_budget) * 0.35
        dinner_budget = float(self.daily_budget) * 0.30
        snack_budget = float(self.daily_budget) * 0.10
        
        meal_plan = {
            'breakfast': self.recommend_meal('breakfast', breakfast_calories, breakfast_budget),
            'lunch': self.recommend_meal('lunch', lunch_calories, lunch_budget),
            'dinner': self.recommend_meal('dinner', dinner_calories, dinner_budget),
            'snacks': self.recommend_meal('snack', snack_calories, snack_budget),
        }
        
        return meal_plan
        
    def recommend_meal(self, meal_type, target_calories, budget):
        """
        Recommend a single meal based on type, calorie target, and budget.
        """
        from .models import Recipe
        
        # Base query - filter by meal type
        recipes = Recipe.objects.filter(meal_type=meal_type)
        
        # Apply dietary restrictions
        if self.user.is_vegetarian:
            recipes = recipes.filter(is_vegetarian=True)
        if self.user.is_vegan:
            recipes = recipes.filter(is_vegan=True)
        if self.user.is_halal:
            recipes = recipes.filter(is_halal=True)
        
        # Filter by health conditions
        if self.user.has_diabetes:
            recipes = recipes.filter(
                ingredients__food__suitable_for_diabetes=True
            ).distinct()
        
        if self.user.has_hypertension:
            recipes = recipes.filter(
                ingredients__food__suitable_for_hypertension=True
            ).distinct()
        
        # Filter by allergies
        if self.user.allergies:
            allergens = [a.strip().lower() for a in self.user.allergies.split(',')]
            for allergen in allergens:
                recipes = recipes.exclude(
                    ingredients__food__name__icontains=allergen
                )
        
        # Score each recipe
        scored_recipes = []
        for recipe in recipes:
            score = self._calculate_recipe_score(
                recipe, 
                target_calories, 
                budget
            )
            scored_recipes.append((recipe, score))
        
        # Sort by score (highest first)
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 3 recommendations
        return [
            {
                'recipe': recipe,
                'score': score,
                'calories_per_serving': recipe.calories_per_serving(),
                'cost_per_serving': recipe.cost_per_serving(),
                'match_percentage': min(score * 10, 100)  # Convert to percentage
            }
            for recipe, score in scored_recipes[:3]
        ]
    
    def _calculate_recipe_score(self, recipe, target_calories, budget):
        """
        Calculate a score for how well a recipe matches user needs.
        Higher score = better match
        Score factors:
        - Calorie match (30%)
        - Budget match (25%)
        - Nutritional balance (20%)
        - Popularity (15%)
        - Difficulty (10%)
        """
        score = 0
        
        # Convert to float for calculations
        calories_per_serving = float(recipe.calories_per_serving())
        cost_per_serving = float(recipe.cost_per_serving())
        target_calories = float(target_calories)
        budget = float(budget)
        
        # 1. Calorie match (30 points max)
        calorie_diff = abs(calories_per_serving - target_calories)
        calorie_score = max(0, 30 - (calorie_diff / target_calories * 30))
        score += calorie_score
        
        # 2. Budget match (25 points max)
        if cost_per_serving <= budget:
            budget_score = 25
        else:
            budget_diff = cost_per_serving - budget
            budget_score = max(0, 25 - (budget_diff / budget * 25))
        score += budget_score
        
        # 3. Nutritional balance (20 points max)
        protein_ratio = float(recipe.total_protein) / recipe.servings
        carb_ratio = float(recipe.total_carbs) / recipe.servings
        fat_ratio = float(recipe.total_fats) / recipe.servings
        
        # Ideal ratios (rough guidelines)
        if self.user.health_goal == 'muscle_gain':
            # High protein
            nutrition_score = min(protein_ratio / 40 * 20, 20)
        elif self.user.health_goal == 'lose_weight':
            # Low carb, moderate protein
            nutrition_score = min((protein_ratio / 30 + (100 - carb_ratio) / 100) * 10, 20)
        else:
            # Balanced
            nutrition_score = 15  # Default moderate score
        
        score += nutrition_score
        
        # 4. Popularity (15 points max)
        popularity_score = min(float(recipe.rating) * 3, 15)
        score += popularity_score
        
        # 5. Difficulty preference (10 points max)
        difficulty_scores = {'easy': 10, 'medium': 7, 'hard': 4}
        score += difficulty_scores.get(recipe.difficulty, 7)
        
        return score
    
    def get_alternative_ingredients(self, recipe):
        """
        Suggest cheaper or more available alternatives for recipe ingredients.
        Useful for affordability and availability challenges.
        """
        from .models import Food
        
        alternatives = []
        
        for ingredient in recipe.ingredients.all():
            food = ingredient.food
            
            # Find similar foods in same category that are cheaper
            cheaper_options = Food.objects.filter(
                category=food.category,
                average_price_per_kg__lt=food.average_price_per_kg
            ).exclude(id=food.id)[:3]
            
            if cheaper_options:
                alternatives.append({
                    'original': food,
                    'alternatives': list(cheaper_options),
                    'savings': food.average_price_per_kg - min(
                        [f.average_price_per_kg for f in cheaper_options]
                    )
                })
        
        return alternatives
    
    def get_seasonal_recommendations(self):
        """
        Recommend recipes based on seasonal ingredients for better affordability.
        """
        from .models import Recipe, Food
        
        current_month = date.today().strftime('%b')
        
        # Find seasonal foods
        seasonal_foods = Food.objects.filter(
            is_seasonal=True,
            available_months__icontains=current_month
        )
        
        # Find recipes using seasonal ingredients
        seasonal_recipes = Recipe.objects.filter(
            ingredients__food__in=seasonal_foods
        ).distinct()
        
        # Apply user filters
        if self.user.is_vegetarian:
            seasonal_recipes = seasonal_recipes.filter(is_vegetarian=True)
        if self.user.is_vegan:
            seasonal_recipes = seasonal_recipes.filter(is_vegan=True)
        
        return seasonal_recipes.order_by('-rating')[:10]
    
    def analyze_nutritional_gaps(self):
        """
        Analyze user's recent meal logs to identify nutritional gaps.
        Suggest foods to fill those gaps.
        """
        from .models import UserMealLog, Food
        from datetime import timedelta
        
        # Get last 7 days of meals
        week_ago = date.today() - timedelta(days=7)
        recent_meals = UserMealLog.objects.filter(
            user=self.user,
            date__gte=week_ago
        )
        
        # Calculate total nutrients consumed
        total_protein = 0
        total_iron = 0
        total_calcium = 0
        total_vitamin_a = 0
        
        for log in recent_meals:
            if log.recipe:
                total_protein += log.recipe.total_protein / log.recipe.servings
                
                # Sum micronutrients from ingredients
                for ingredient in log.recipe.ingredients.all():
                    quantity_factor = ingredient.quantity / 100  # nutrients are per 100g
                    if ingredient.food.iron:
                        total_iron += ingredient.food.iron * quantity_factor
                    if ingredient.food.calcium:
                        total_calcium += ingredient.food.calcium * quantity_factor
                    if ingredient.food.vitamin_a:
                        total_vitamin_a += ingredient.food.vitamin_a * quantity_factor
        
        # Daily requirements (rough guidelines)
        days = 7
        protein_needed = 50 * days  # 50g per day
        iron_needed = 18 * days  # 18mg per day (for women)
        calcium_needed = 1000 * days  # 1000mg per day
        vitamin_a_needed = 700 * days  # 700mcg per day
        
        gaps = []
        
        if total_protein < protein_needed * 0.7:
            gaps.append({
                'nutrient': 'Protein',
                'deficit': protein_needed - total_protein,
                'recommendation': Food.objects.filter(
                    protein__gte=20
                ).order_by('-protein')[:5]
            })
        
        if total_iron < iron_needed * 0.7:
            gaps.append({
                'nutrient': 'Iron',
                'deficit': iron_needed - total_iron,
                'recommendation': Food.objects.filter(
                    iron__gte=2
                ).order_by('-iron')[:5]
            })
        
        return gaps
    
    def suggest_grocery_list(self, meal_plan_days=7):
        """
        Generate a grocery list for multiple days of meal plans.
        Groups by food items and calculates total quantities needed.
        """
        from collections import defaultdict
        
        # Generate meal plans for the week
        grocery_dict = defaultdict(lambda: {'quantity': 0, 'cost': 0})
        
        for day in range(meal_plan_days):
            target_date = date.today() + timedelta(days=day)
            daily_plan = self.generate_daily_meal_plan(target_date)
            
            # Collect ingredients from all meals
            for meal_type, recipes in daily_plan.items():
                if not recipes:
                    continue
                    
                # Handle single recipe or list of recommendations
                recipe_list = recipes if isinstance(recipes, list) else [recipes]
                
                for item in recipe_list:
                    recipe = item['recipe'] if isinstance(item, dict) else item
                    
                    for ingredient in recipe.ingredients.all():
                        food_name = ingredient.food.name
                        grocery_dict[food_name]['quantity'] += float(ingredient.quantity)
                        grocery_dict[food_name]['cost'] += (
                            float(ingredient.food.average_price_per_kg) * 
                            float(ingredient.quantity) / 1000
                        )
                        grocery_dict[food_name]['unit'] = 'g'
        
        # Convert to list format
        grocery_list = [
            {
                'item': name,
                'quantity': data['quantity'],
                'unit': data['unit'],
                'estimated_cost': round(data['cost'], 2)
            }
            for name, data in grocery_dict.items()
        ]
        
        # Sort by cost (most expensive first)
        grocery_list.sort(key=lambda x: x['estimated_cost'], reverse=True)
        
        total_cost = sum(item['estimated_cost'] for item in grocery_list)
        
        return {
            'items': grocery_list,
            'total_cost': round(total_cost, 2),
            'days': meal_plan_days
        }