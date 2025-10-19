# serializers.py - API serializers

from rest_framework import serializers
from .models import (
    User, Food, Recipe, RecipeIngredient, MealPlan, 
    UserMealLog, HealthTip, FoodCategory
)


class UserProfileSerializer(serializers.ModelSerializer):
    bmi = serializers.SerializerMethodField()
    daily_calories = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone_number', 'date_of_birth',
            'gender', 'location', 'height', 'weight', 'activity_level',
            'health_goal', 'is_vegetarian', 'is_vegan', 'is_halal',
            'daily_budget', 'has_diabetes', 'has_hypertension', 'allergies',
            'bmi', 'daily_calories'
        ]
        read_only_fields = ['id', 'bmi', 'daily_calories']
    
    def get_bmi(self, obj):
        return obj.calculate_bmi()
    
    def get_daily_calories(self, obj):
        return obj.calculate_daily_calories()


class FoodSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Food
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)
    food_details = FoodSerializer(source='food', read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'food', 'food_name', 'food_details', 'quantity', 'notes']


class RecipeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for recipe lists"""
    calories_per_serving = serializers.SerializerMethodField()
    cost_per_serving = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'local_name', 'description', 'meal_type',
            'difficulty', 'prep_time', 'cook_time', 'servings',
            'estimated_cost', 'rating', 'times_made', 'image_url',
            'calories_per_serving', 'cost_per_serving',
            'is_vegetarian', 'is_vegan', 'is_halal'
        ]
    
    def get_calories_per_serving(self, obj):
        return obj.calories_per_serving()
    
    def get_cost_per_serving(self, obj):
        return float(obj.cost_per_serving())


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with ingredients"""
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    calories_per_serving = serializers.SerializerMethodField()
    cost_per_serving = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = '__all__'
    
    def get_calories_per_serving(self, obj):
        return obj.calories_per_serving()
    
    def get_cost_per_serving(self, obj):
        return float(obj.cost_per_serving())


class MealPlanSerializer(serializers.ModelSerializer):
    breakfast_details = RecipeListSerializer(source='breakfast', read_only=True)
    lunch_details = RecipeListSerializer(source='lunch', read_only=True)
    dinner_details = RecipeListSerializer(source='dinner', read_only=True)
    snacks_details = RecipeListSerializer(source='snacks', many=True, read_only=True)
    
    class Meta:
        model = MealPlan
        fields = [
            'id', 'user', 'date', 'breakfast', 'breakfast_details',
            'lunch', 'lunch_details', 'dinner', 'dinner_details',
            'snacks', 'snacks_details', 'total_calories', 'total_cost',
            'is_followed', 'created_at'
        ]
        read_only_fields = ['total_calories', 'total_cost']


class UserMealLogSerializer(serializers.ModelSerializer):
    recipe_details = RecipeListSerializer(source='recipe', read_only=True)
    
    class Meta:
        model = UserMealLog
        fields = ['id', 'user', 'recipe', 'recipe_details', 'meal_type', 'date', 'notes', 'created_at']


class HealthTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTip
        fields = '__all__'