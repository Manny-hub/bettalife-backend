# seed_data.py - Populate database with Nigerian food data

from decimal import Decimal
from apps.nutrition.models import (
    FoodCategory, Food, Recipe, RecipeIngredient, HealthTip
)


def seed_food_categories():
    """Create food categories"""
    categories = [
        {'name': 'Grains & Starches', 'description': 'Rice, yam, cassava, plantain'},
        {'name': 'Proteins', 'description': 'Fish, meat, eggs, beans'},
        {'name': 'Vegetables', 'description': 'Leafy greens, peppers, tomatoes'},
        {'name': 'Fruits', 'description': 'Local and seasonal fruits'},
        {'name': 'Oils & Fats', 'description': 'Palm oil, groundnut oil'},
        {'name': 'Legumes', 'description': 'Beans, lentils, groundnuts'},
        {'name': 'Spices & Seasonings', 'description': 'Local spices and seasonings'},
        {'name': 'Dairy & Alternatives', 'description': 'Milk, yogurt, cheese'},
    ]
    
    for cat_data in categories:
        FoodCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
    
    print("✓ Food categories created")


def seed_foods():
    """Create sample Nigerian foods with nutritional data"""
    
    # Get categories
    grains = FoodCategory.objects.get(name='Grains & Starches')
    proteins = FoodCategory.objects.get(name='Proteins')
    vegetables = FoodCategory.objects.get(name='Vegetables')
    legumes = FoodCategory.objects.get(name='Legumes')
    oils = FoodCategory.objects.get(name='Oils & Fats')
    
    foods_data = [
        # Grains & Starches
        {
            'name': 'White Rice',
            'local_name': 'Shinkafa',
            'category': grains,
            'calories': Decimal('130'),
            'protein': Decimal('2.7'),
            'carbohydrates': Decimal('28'),
            'fats': Decimal('0.3'),
            'fiber': Decimal('0.4'),
            'average_price_per_kg': Decimal('800'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': False,
            'iron': Decimal('0.8'),
            'calcium': Decimal('10'),
        },
        {
            'name': 'Yam',
            'local_name': 'Ji/Isu',
            'category': grains,
            'calories': Decimal('118'),
            'protein': Decimal('1.5'),
            'carbohydrates': Decimal('27.9'),
            'fats': Decimal('0.2'),
            'fiber': Decimal('4.1'),
            'average_price_per_kg': Decimal('600'),
            'is_vegetarian': True,
            'is_vegan': True,
            'is_seasonal': True,
            'available_months': 'Jan,Feb,Mar,Aug,Sep,Oct,Nov,Dec',
            'iron': Decimal('0.5'),
            'calcium': Decimal('17'),
        },
        {
            'name': 'Plantain',
            'local_name': 'Ogede/Ayaba',
            'category': grains,
            'calories': Decimal('122'),
            'protein': Decimal('1.3'),
            'carbohydrates': Decimal('31.9'),
            'fats': Decimal('0.4'),
            'fiber': Decimal('2.3'),
            'average_price_per_kg': Decimal('350'),
            'is_vegetarian': True,
            'is_vegan': True,
            'vitamin_a': Decimal('1127'),
        },
        
        # Proteins
        {
            'name': 'Chicken',
            'local_name': 'Kaza/Adiye',
            'category': proteins,
            'calories': Decimal('239'),
            'protein': Decimal('27'),
            'carbohydrates': Decimal('0'),
            'fats': Decimal('14'),
            'fiber': Decimal('0'),
            'average_price_per_kg': Decimal('2500'),
            'is_vegetarian': False,
            'is_vegan': False,
            'suitable_for_hypertension': True,
            'iron': Decimal('0.9'),
        },
        {
            'name': 'Mackerel (Titus)',
            'local_name': 'Titus',
            'category': proteins,
            'calories': Decimal('205'),
            'protein': Decimal('19'),
            'carbohydrates': Decimal('0'),
            'fats': Decimal('14'),
            'fiber': Decimal('0'),
            'average_price_per_kg': Decimal('1800'),
            'is_vegetarian': False,
            'is_vegan': False,
            'iron': Decimal('1.6'),
        },
        {
            'name': 'Eggs',
            'local_name': 'Kwai/Eyin',
            'category': proteins,
            'calories': Decimal('155'),
            'protein': Decimal('13'),
            'carbohydrates': Decimal('1.1'),
            'fats': Decimal('11'),
            'fiber': Decimal('0'),
            'average_price_per_kg': Decimal('1400'),
            'is_vegetarian': True,
            'is_vegan': False,
            'iron': Decimal('1.8'),
            'calcium': Decimal('56'),
        },
        
        # Legumes
        {
            'name': 'Black-eyed Peas',
            'local_name': 'Wake/Ewa',
            'category': legumes,
            'calories': Decimal('116'),
            'protein': Decimal('8'),
            'carbohydrates': Decimal('21'),
            'fats': Decimal('0.5'),
            'fiber': Decimal('6'),
            'average_price_per_kg': Decimal('800'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': True,
            'iron': Decimal('2.5'),
            'calcium': Decimal('24'),
        },
        {
            'name': 'Groundnuts (Peanuts)',
            'local_name': 'Gyada/Epa',
            'category': legumes,
            'calories': Decimal('567'),
            'protein': Decimal('26'),
            'carbohydrates': Decimal('16'),
            'fats': Decimal('49'),
            'fiber': Decimal('8.5'),
            'average_price_per_kg': Decimal('1000'),
            'is_vegetarian': True,
            'is_vegan': True,
            'iron': Decimal('4.6'),
            'calcium': Decimal('92'),
        },
        
        # Vegetables
        {
            'name': 'Spinach',
            'local_name': 'Alayyahu/Efo tete',
            'category': vegetables,
            'calories': Decimal('23'),
            'protein': Decimal('2.9'),
            'carbohydrates': Decimal('3.6'),
            'fats': Decimal('0.4'),
            'fiber': Decimal('2.2'),
            'average_price_per_kg': Decimal('200'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': True,
            'suitable_for_hypertension': True,
            'iron': Decimal('2.7'),
            'calcium': Decimal('99'),
            'vitamin_a': Decimal('9377'),
        },
        {
            'name': 'Tomatoes',
            'local_name': 'Tumatir/Tomato',
            'category': vegetables,
            'calories': Decimal('18'),
            'protein': Decimal('0.9'),
            'carbohydrates': Decimal('3.9'),
            'fats': Decimal('0.2'),
            'fiber': Decimal('1.2'),
            'average_price_per_kg': Decimal('300'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': True,
            'suitable_for_hypertension': True,
            'vitamin_a': Decimal('833'),
        },
        {
            'name': 'Bell Peppers',
            'local_name': 'Tatase',
            'category': vegetables,
            'calories': Decimal('31'),
            'protein': Decimal('1'),
            'carbohydrates': Decimal('6'),
            'fats': Decimal('0.3'),
            'fiber': Decimal('2.1'),
            'average_price_per_kg': Decimal('500'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': True,
            'suitable_for_hypertension': True,
            'vitamin_a': Decimal('3131'),
        },
        {
            'name': 'Onions',
            'local_name': 'Albasa/Alubosa',
            'category': vegetables,
            'calories': Decimal('40'),
            'protein': Decimal('1.1'),
            'carbohydrates': Decimal('9.3'),
            'fats': Decimal('0.1'),
            'fiber': Decimal('1.7'),
            'average_price_per_kg': Decimal('400'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': True,
            'suitable_for_hypertension': True,
        },
        
        # Oils
        {
            'name': 'Palm Oil',
            'local_name': 'Man gyada/Epo pupa',
            'category': oils,
            'calories': Decimal('884'),
            'protein': Decimal('0'),
            'carbohydrates': Decimal('0'),
            'fats': Decimal('100'),
            'fiber': Decimal('0'),
            'average_price_per_kg': Decimal('1500'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_diabetes': True,
            'suitable_for_hypertension': False,
            'vitamin_a': Decimal('30000'),
        },
        {
            'name': 'Groundnut Oil',
            'local_name': 'Man gyada/Epo epa',
            'category': oils,
            'calories': Decimal('884'),
            'protein': Decimal('0'),
            'carbohydrates': Decimal('0'),
            'fats': Decimal('100'),
            'fiber': Decimal('0'),
            'average_price_per_kg': Decimal('2000'),
            'is_vegetarian': True,
            'is_vegan': True,
            'suitable_for_hypertension': True,
        },
    ]
    
    for food_data in foods_data:
        Food.objects.get_or_create(
            name=food_data['name'],
            defaults=food_data
        )
    
    print(f"✓ {len(foods_data)} foods created")


def seed_recipes():
    """Create sample Nigerian recipes"""
    
    recipes_data = [
        {
            'name': 'Jollof Rice',
            'local_name': 'Jollof',
            'description': 'Popular West African one-pot rice dish',
            'meal_type': 'lunch',
            'difficulty': 'medium',
            'prep_time': 20,
            'cook_time': 45,
            'servings': 4,
            'instructions': 'Cook rice with tomato sauce and spices',
            'estimated_cost': Decimal('1500'),
            'total_calories': Decimal('1600'),
            'total_protein': Decimal('20'),
            'total_carbs': Decimal('320'),
            'total_fats': Decimal('20'),
            'rating': Decimal('4.8'),
            'times_made': 1250,
            'ingredients': [
                ('White Rice', 400),
                ('Tomatoes', 300),
                ('Bell Peppers', 150),
                ('Onions', 100),
                ('Groundnut Oil', 50),
            ]
        },
        {
            'name': 'Moi Moi',
            'local_name': 'Moi Moi',
            'description': 'Steamed bean pudding',
            'meal_type': 'breakfast',
            'difficulty': 'medium',
            'prep_time': 30,
            'cook_time': 45,
            'servings': 6,
            'instructions': 'Blend beans, steam in containers',
            'estimated_cost': Decimal('800'),
            'total_calories': Decimal('1400'),
            'total_protein': Decimal('96'),
            'total_carbs': Decimal('180'),
            'total_fats': Decimal('30'),
            'rating': Decimal('4.7'),
            'times_made': 980,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Black-eyed Peas', 500),
                ('Bell Peppers', 100),
                ('Onions', 80),
                ('Groundnut Oil', 40),
            ]
        },
        {
            'name': 'Fried Plantain',
            'local_name': 'Dodo',
            'description': 'Sweet fried ripe plantain',
            'meal_type': 'snack',
            'difficulty': 'easy',
            'prep_time': 5,
            'cook_time': 10,
            'servings': 3,
            'instructions': 'Slice and fry plantain until golden',
            'estimated_cost': Decimal('400'),
            'total_calories': Decimal('800'),
            'total_protein': Decimal('4'),
            'total_carbs': Decimal('160'),
            'total_fats': Decimal('30'),
            'rating': Decimal('4.6'),
            'times_made': 2100,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Plantain', 600),
                ('Groundnut Oil', 50),
            ]
        },
    ]
    
    for recipe_data in recipes_data:
        ingredients_list = recipe_data.pop('ingredients')
        
        recipe, created = Recipe.objects.get_or_create(
            name=recipe_data['name'],
            defaults=recipe_data
        )
        
        if created:
            # Add ingredients
            for food_name, quantity in ingredients_list:
                try:
                    food = Food.objects.get(name=food_name)
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        food=food,
                        quantity=Decimal(str(quantity))
                    )
                except Food.DoesNotExist:
                    print(f"Warning: Food '{food_name}' not found for recipe '{recipe.name}'")
    
    print(f"✓ {len(recipes_data)} recipes created")


def seed_health_tips():
    """Create health and nutrition tips"""
    
    tips = [
        {
            'title': 'Importance of Protein in Your Diet',
            'content': 'Protein is essential for building tissues. Good sources: beans, fish, eggs.',
            'category': 'Nutrition',
            'relevant_for_weight_loss': True,
        },
        {
            'title': 'Managing Diabetes with Nigerian Foods',
            'content': 'Choose brown rice over white rice, eat more beans and vegetables.',
            'category': 'Health',
            'relevant_for_diabetes': True,
        },
        {
            'title': 'Reducing Salt for Better Blood Pressure',
            'content': 'Use less seasoning cubes, add more natural spices like ginger.',
            'category': 'Health',
            'relevant_for_hypertension': True,
        },
    ]
    
    for tip_data in tips:
        HealthTip.objects.get_or_create(
            title=tip_data['title'],
            defaults=tip_data
        )
    
    print(f"✓ {len(tips)} health tips created")


def run_seed():
    """Run all seed functions"""
    print("\n🌱 Starting database seeding...\n")
    
    seed_food_categories()
    seed_foods()
    seed_recipes()
    seed_health_tips()
    
    print("\n✅ Database seeding completed successfully!\n")
    print("Summary:")
    print(f"  - Food Categories: {FoodCategory.objects.count()}")
    print(f"  - Foods: {Food.objects.count()}")
    print(f"  - Recipes: {Recipe.objects.count()}")
    print(f"  - Health Tips: {HealthTip.objects.count()}")


if __name__ == '__main__':
    run_seed()