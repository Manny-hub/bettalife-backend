from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, FoodCategory, Food, Recipe, RecipeIngredient,
    MealPlan, UserMealLog, HealthTip
)


# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model with health profile fields"""
    
    # Fields to display in the list view
    list_display = ['username', 'email', 'health_goal', 'weight', 'height', 'daily_budget']
    list_filter = ['health_goal', 'is_vegetarian', 'is_vegan', 'has_diabetes', 'has_hypertension']
    
    # Add health fields to the user edit form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Health Profile', {
            'fields': (
                'phone_number', 'date_of_birth', 'gender', 'location',
                'height', 'weight', 'activity_level', 'health_goal'
            )
        }),
        ('Dietary Preferences', {
            'fields': ('is_vegetarian', 'is_vegan', 'is_halal', 'daily_budget')
        }),
        ('Health Conditions', {
            'fields': ('has_diabetes', 'has_hypertension', 'allergies')
        }),
    )
    
    # Fields for creating new user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Health Profile', {
            'fields': (
                'phone_number', 'date_of_birth', 'gender', 'location',
                'height', 'weight', 'activity_level', 'health_goal'
            )
        }),
    )


# Food Category Admin
@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


# Food Admin
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'local_name', 'category', 'calories', 
        'protein', 'average_price_per_kg', 'is_vegetarian'
    ]
    list_filter = [
        'category', 'is_vegetarian', 'is_vegan', 
        'suitable_for_diabetes', 'suitable_for_hypertension', 'is_seasonal'
    ]
    search_fields = ['name', 'local_name']
    ordering = ['name']


# Recipe Ingredient Inline (shows ingredients inside Recipe admin)
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ['food']


# Recipe Admin
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'local_name', 'meal_type', 'difficulty', 
        'prep_time', 'cook_time', 'servings', 'rating', 'times_made'
    ]
    list_filter = ['meal_type', 'difficulty', 'is_vegetarian', 'is_vegan']
    search_fields = ['name', 'local_name', 'description']
    inlines = [RecipeIngredientInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'local_name', 'description', 'meal_type', 'difficulty')
        }),
        ('Cooking Details', {
            'fields': ('prep_time', 'cook_time', 'servings', 'instructions')
        }),
        ('Nutritional Info', {
            'fields': ('total_calories', 'total_protein', 'total_carbs', 'total_fats')
        }),
        ('Cost & Ratings', {
            'fields': ('estimated_cost', 'rating', 'times_made')
        }),
        ('Dietary Tags', {
            'fields': ('is_vegetarian', 'is_vegan', 'is_halal')
        }),
        ('Media', {
            'fields': ('image_url',)
        }),
    )


# Meal Plan Admin
@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'date', 'breakfast', 'lunch', 'dinner', 
        'total_calories', 'total_cost', 'is_followed'
    ]
    list_filter = ['date', 'is_followed']
    search_fields = ['user__username']
    date_hierarchy = 'date'
    raw_id_fields = ['user', 'breakfast', 'lunch', 'dinner']
    filter_horizontal = ['snacks']


# User Meal Log Admin
@admin.register(UserMealLog)
class UserMealLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'meal_type', 'date', 'created_at']
    list_filter = ['meal_type', 'date']
    search_fields = ['user__username', 'recipe__name']
    date_hierarchy = 'date'
    raw_id_fields = ['user', 'recipe']


# Health Tip Admin
@admin.register(HealthTip)
class HealthTipAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'relevant_for_diabetes', 
        'relevant_for_hypertension', 'relevant_for_weight_loss'
    ]
    list_filter = [
        'category', 'relevant_for_diabetes', 
        'relevant_for_hypertension', 'relevant_for_weight_loss'
    ]
    search_fields = ['title', 'content']