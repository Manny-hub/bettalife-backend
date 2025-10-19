# models.py - Core models for Nigerian Food Recommendation App

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Extended user model with health profile"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    ACTIVITY_LEVEL = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Light (exercise 1-3 days/week)'),
        ('moderate', 'Moderate (exercise 3-5 days/week)'),
        ('active', 'Active (exercise 6-7 days/week)'),
        ('very_active', 'Very Active (physical job or training twice per day)'),
    ]
    
    GOAL_CHOICES = [
        ('lose_weight', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain_weight', 'Gain Weight'),
        ('muscle_gain', 'Build Muscle'),
        ('general_health', 'General Health'),
    ]
    
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)  # Lagos, Abuja, etc.
    
    # Health metrics
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL, default='moderate')
    health_goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default='general_health')
    
    # Dietary preferences
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_halal = models.BooleanField(default=True)  # Default true for Nigerian market
    
    # Budget
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Daily food budget in Naira")
    
    # Health conditions
    has_diabetes = models.BooleanField(default=False)
    has_hypertension = models.BooleanField(default=False)
    allergies = models.TextField(blank=True, help_text="Comma-separated list of allergies")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = float(self.height) / 100
            return float(self.weight) / (height_m ** 2)
        return None
    
    def calculate_daily_calories(self):
        """Calculate recommended daily calories based on Harris-Benedict equation"""
        if not all([self.weight, self.height, self.date_of_birth, self.gender]):
            return 2000  # Default
        
        from datetime import date
        age = (date.today() - self.date_of_birth).days // 365
        
        # Basal Metabolic Rate
        if self.gender == 'M':
            bmr = 88.362 + (13.397 * float(self.weight)) + (4.799 * float(self.height)) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * float(self.weight)) + (3.098 * float(self.height)) - (4.330 * age)
        
        # Activity multiplier
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        daily_calories = bmr * multipliers.get(self.activity_level, 1.55)
        
        # Adjust based on goal
        if self.health_goal == 'lose_weight':
            daily_calories *= 0.85  # 15% deficit
        elif self.health_goal == 'gain_weight':
            daily_calories *= 1.15  # 15% surplus
        
        return round(daily_calories)


class FoodCategory(models.Model):
    """Categories of Nigerian foods"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Food Categories"
    
    def __str__(self):
        return self.name


class Food(models.Model):
    """Nigerian food items with nutritional information"""
    name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=200, blank=True, help_text="Name in local language")
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name='foods')
    description = models.TextField(blank=True)
    
    # Nutritional info per 100g
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2, help_text="Grams per 100g")
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, help_text="Grams per 100g")
    fats = models.DecimalField(max_digits=5, decimal_places=2, help_text="Grams per 100g")
    fiber = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Grams per 100g")
    
    # Micronutrients (optional but important for African context)
    iron = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="mg per 100g")
    calcium = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="mg per 100g")
    vitamin_a = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="mcg per 100g")
    
    # Availability and cost
    is_seasonal = models.BooleanField(default=False)
    available_months = models.CharField(max_length=100, blank=True, help_text="e.g., Jan,Feb,Mar")
    average_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Naira")
    
    # Tags for filtering
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_halal = models.BooleanField(default=True)
    is_gluten_free = models.BooleanField(default=True)
    
    # Health considerations
    suitable_for_diabetes = models.BooleanField(default=True)
    suitable_for_hypertension = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Nigerian recipes"""
    MEAL_TYPE = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    
    DIFFICULTY = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='medium')
    
    # Cooking details
    prep_time = models.IntegerField(help_text="Preparation time in minutes")
    cook_time = models.IntegerField(help_text="Cooking time in minutes")
    servings = models.IntegerField(default=4)
    
    instructions = models.TextField(help_text="Step-by-step cooking instructions")
    
    # Cost and nutritional info (calculated from ingredients)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total cost in Naira")
    total_calories = models.DecimalField(max_digits=8, decimal_places=2)
    total_protein = models.DecimalField(max_digits=6, decimal_places=2)
    total_carbs = models.DecimalField(max_digits=6, decimal_places=2)
    total_fats = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Image
    image_url = models.URLField(blank=True)
    
    # Tags
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_halal = models.BooleanField(default=True)
    
    # Popularity
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    times_made = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calories_per_serving(self):
        return self.total_calories / self.servings
    
    def cost_per_serving(self):
        return self.estimated_cost / self.servings
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Ingredients for each recipe"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, help_text="Quantity in grams")
    notes = models.CharField(max_length=200, blank=True, help_text="e.g., 'chopped', 'diced'")
    
    def __str__(self):
        return f"{self.quantity}g {self.food.name} for {self.recipe.name}"


class MealPlan(models.Model):
    """Daily meal plans for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    date = models.DateField()
    
    breakfast = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, related_name='breakfast_plans')
    lunch = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, related_name='lunch_plans')
    dinner = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, related_name='dinner_plans')
    snacks = models.ManyToManyField(Recipe, blank=True, related_name='snack_plans')
    
    total_calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_followed = models.BooleanField(default=False, help_text="Did user follow this plan?")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def calculate_totals(self):
        """Calculate total calories and cost for the day"""
        total_cal = 0
        total_cost = 0
        
        for meal in [self.breakfast, self.lunch, self.dinner]:
            if meal:
                total_cal += meal.calories_per_serving()
                total_cost += meal.cost_per_serving()
        
        for snack in self.snacks.all():
            total_cal += snack.calories_per_serving()
            total_cost += snack.cost_per_serving()
        
        self.total_calories = total_cal
        self.total_cost = total_cost
        self.save()
    
    def __str__(self):
        return f"Meal plan for {self.user.username} on {self.date}"


class UserMealLog(models.Model):
    """Track what users actually eat"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_logs')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    meal_type = models.CharField(max_length=20, choices=Recipe.MEAL_TYPE)
    date = models.DateField()
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}"


class HealthTip(models.Model):
    """Educational content about nutrition and health"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    
    # Target audience
    relevant_for_diabetes = models.BooleanField(default=False)
    relevant_for_hypertension = models.BooleanField(default=False)
    relevant_for_weight_loss = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title