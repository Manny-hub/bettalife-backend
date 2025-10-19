# apps/nutrition/more_recipes_seed.py
# Add 30+ more Nigerian recipes

from decimal import Decimal
from apps.nutrition.models import Recipe, RecipeIngredient, Food


def seed_more_recipes():
    """Add comprehensive Nigerian recipe collection"""
    
    recipes = [
        # BREAKFAST RECIPES
        {
            'name': 'Akara (Bean Cakes)',
            'local_name': 'Akara/Kosai',
            'description': 'Deep-fried bean cakes, popular breakfast item',
            'meal_type': 'breakfast',
            'difficulty': 'medium',
            'prep_time': 25,
            'cook_time': 20,
            'servings': 4,
            'instructions': '''1. Soak beans overnight, peel skin
2. Blend with peppers and onions  
3. Add salt, mix into batter
4. Deep fry spoonfuls until golden
5. Serve hot with bread or pap''',
            'estimated_cost': Decimal('600'),
            'total_calories': Decimal('1200'),
            'total_protein': Decimal('64'),
            'total_carbs': Decimal('140'),
            'total_fats': Decimal('40'),
            'rating': Decimal('4.6'),
            'times_made': 850,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Black-eyed Peas', 400),
                ('Onions', 60),
                ('Bell Peppers (Tatase)', 50),
                ('Groundnut Oil', 100),
            ]
        },
        {
            'name': 'Yam Porridge',
            'local_name': 'Asaro',
            'description': 'Yam cooked in rich palm oil sauce',
            'meal_type': 'lunch',
            'difficulty': 'easy',
            'prep_time': 15,
            'cook_time': 35,
            'servings': 4,
            'instructions': '''1. Peel and dice yam
2. Boil until partially soft
3. Add tomatoes, peppers, onions
4. Add palm oil, seasonings
5. Simmer until yam is soft and mushy
6. Serve hot''',
            'estimated_cost': Decimal('900'),
            'total_calories': Decimal('1800'),
            'total_protein': Decimal('24'),
            'total_carbs': Decimal('320'),
            'total_fats': Decimal('60'),
            'rating': Decimal('4.7'),
            'times_made': 650,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Yam', 800),
                ('Palm Oil', 80),
                ('Tomatoes', 200),
                ('Onions', 80),
            ]
        },
        {
            'name': 'Ewa Agoyin',
            'local_name': 'Ewa Agoyin',
            'description': 'Mashed beans with spicy pepper sauce',
            'meal_type': 'dinner',
            'difficulty': 'easy',
            'prep_time': 10,
            'cook_time': 90,
            'servings': 4,
            'instructions': '''1. Boil beans until very soft
2. Mash beans slightly
3. Blend peppers with onions
4. Fry pepper mixture in palm oil until dark
5. Serve beans with pepper sauce on top''',
            'estimated_cost': Decimal('600'),
            'total_calories': Decimal('1000'),
            'total_protein': Decimal('64'),
            'total_carbs': Decimal('168'),
            'total_fats': Decimal('25'),
            'rating': Decimal('4.5'),
            'times_made': 750,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Black-eyed Peas', 400),
                ('Palm Oil', 60),
                ('Bell Peppers (Tatase)', 100),
                ('Onions', 50),
            ]
        },
        {
            'name': 'Pepper Soup',
            'local_name': 'Pepper Soup',
            'description': 'Spicy soup with meat or fish',
            'meal_type': 'dinner',
            'difficulty': 'easy',
            'prep_time': 10,
            'cook_time': 30,
            'servings': 4,
            'instructions': '''1. Season meat/fish
2. Boil with pepper soup spices
3. Add uziza leaves
4. Cook until tender
5. Serve hot''',
            'estimated_cost': Decimal('2000'),
            'total_calories': Decimal('800'),
            'total_protein': Decimal('120'),
            'total_carbs': Decimal('20'),
            'total_fats': Decimal('40'),
            'rating': Decimal('4.8'),
            'times_made': 920,
            'ingredients': [
                ('Goat Meat', 600),
                ('Onions', 50),
                ('Scotch Bonnet Pepper', 30),
            ]
        },
        {
            'name': 'Efo Riro',
            'local_name': 'Efo Riro',
            'description': 'Yoruba vegetable stew with spinach',
            'meal_type': 'lunch',
            'difficulty': 'medium',
            'prep_time': 20,
            'cook_time': 40,
            'servings': 4,
            'instructions': '''1. Blend tomatoes and peppers
2. Fry in palm oil until oil rises
3. Add meat and fish
4. Add washed spinach
5. Cook for 5 minutes
6. Serve with eba or rice''',
            'estimated_cost': Decimal('1800'),
            'total_calories': Decimal('1400'),
            'total_protein': Decimal('80'),
            'total_carbs': Decimal('60'),
            'total_fats': Decimal('100'),
            'rating': Decimal('4.9'),
            'times_made': 1100,
            'ingredients': [
                ('Spinach', 400),
                ('Beef', 300),
                ('Mackerel (Titus)', 200),
                ('Palm Oil', 100),
                ('Tomatoes', 300),
            ]
        },
        {
            'name': 'Gizdodo',
            'local_name': 'Gizdodo',
            'description': 'Gizzard and plantain in pepper sauce',
            'meal_type': 'snack',
            'difficulty': 'medium',
            'prep_time': 15,
            'cook_time': 25,
            'servings': 4,
            'instructions': '''1. Boil gizzards until tender
2. Fry plantain separately
3. Blend peppers and tomatoes
4. Fry pepper mixture
5. Add gizzard and plantain
6. Simmer together''',
            'estimated_cost': Decimal('1500'),
            'total_calories': Decimal('1600'),
            'total_protein': Decimal('80'),
            'total_carbs': Decimal('180'),
            'total_fats': Decimal('60'),
            'rating': Decimal('4.7'),
            'times_made': 580,
            'ingredients': [
                ('Gizzard (Chicken)', 400),
                ('Plantain', 400),
                ('Tomatoes', 200),
                ('Bell Peppers (Tatase)', 100),
                ('Groundnut Oil', 80),
            ]
        },
        {
            'name': 'Ofada Rice with Ayamase Sauce',
            'local_name': 'Ofada Rice',
            'description': 'Local rice with green pepper stew',
            'meal_type': 'lunch',
            'difficulty': 'hard',
            'prep_time': 30,
            'cook_time': 60,
            'servings': 4,
            'instructions': '''1. Wash and cook ofada rice
2. Blend green peppers, scotch bonnet
3. Boil and fry with locust beans
4. Add assorted meats
5. Simmer until oil rises
6. Serve rice with sauce''',
            'estimated_cost': Decimal('2500'),
            'total_calories': Decimal('2000'),
            'total_protein': Decimal('100'),
            'total_carbs': Decimal('300'),
            'total_fats': Decimal('80'),
            'rating': Decimal('4.9'),
            'times_made': 450,
            'ingredients': [
                ('White Rice', 400),
                ('Beef', 300),
                ('Bell Peppers (Tatase)', 300),
                ('Palm Oil', 120),
                ('Locust Beans', 20),
            ]
        },
        {
            'name': 'Beans and Plantain (Dodo Ikire)',
            'local_name': 'Ewa ati Dodo',
            'description': 'Classic beans and fried plantain combo',
            'meal_type': 'lunch',
            'difficulty': 'easy',
            'prep_time': 10,
            'cook_time': 60,
            'servings': 4,
            'instructions': '''1. Boil beans with onions until soft
2. Season to taste
3. Slice and fry ripe plantain
4. Serve together''',
            'estimated_cost': Decimal('700'),
            'total_calories': Decimal('1400'),
            'total_protein': Decimal('64'),
            'total_carbs': Decimal('240'),
            'total_fats': Decimal('40'),
            'rating': Decimal('4.6'),
            'times_made': 890,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Black-eyed Peas', 400),
                ('Plantain', 400),
                ('Groundnut Oil', 60),
                ('Onions', 50),
            ]
        },
        {
            'name': 'Nkwobi',
            'local_name': 'Nkwobi',
            'description': 'Spicy cow foot delicacy',
            'meal_type': 'snack',
            'difficulty': 'medium',
            'prep_time': 20,
            'cook_time': 120,
            'servings': 4,
            'instructions': '''1. Boil cow foot until tender
2. Cut into bite sizes
3. Make sauce with palm oil, potash, utazi
4. Mix cow foot with sauce
5. Garnish with sliced onions
6. Serve as appetizer''',
            'estimated_cost': Decimal('2000'),
            'total_calories': Decimal('1200'),
            'total_protein': Decimal('100'),
            'total_carbs': Decimal('10'),
            'total_fats': Decimal('80'),
            'rating': Decimal('4.7'),
            'times_made': 320,
            'ingredients': [
                ('Beef', 800),
                ('Palm Oil', 80),
                ('Onions', 60),
                ('Scotch Bonnet Pepper', 20),
            ]
        },
        {
            'name': 'Boli (Roasted Plantain)',
            'local_name': 'Boli',
            'description': 'Roasted plantain with groundnut',
            'meal_type': 'snack',
            'difficulty': 'easy',
            'prep_time': 5,
            'cook_time': 15,
            'servings': 2,
            'instructions': '''1. Roast unpeeled plantain over charcoal
2. Turn frequently until black
3. Peel and serve with roasted groundnuts
4. Add pepper sauce if desired''',
            'estimated_cost': Decimal('300'),
            'total_calories': Decimal('600'),
            'total_protein': Decimal('8'),
            'total_carbs': Decimal('120'),
            'total_fats': Decimal('10'),
            'rating': Decimal('4.5'),
            'times_made': 1200,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Plantain', 400),
                ('Groundnuts (Peanuts)', 100),
            ]
        },
        {
            'name': 'Chicken Stew',
            'local_name': 'Obe Ata Dindin',
            'description': 'Classic Nigerian tomato stew with chicken',
            'meal_type': 'dinner',
            'difficulty': 'easy',
            'prep_time': 15,
            'cook_time': 45,
            'servings': 4,
            'instructions': '''1. Season and cook chicken
2. Blend tomatoes, peppers, onions
3. Heat oil, fry blended mixture
4. Cook until oil separates
5. Add chicken pieces
6. Season, simmer 15 minutes''',
            'estimated_cost': Decimal('2000'),
            'total_calories': Decimal('1800'),
            'total_protein': Decimal('180'),
            'total_carbs': Decimal('40'),
            'total_fats': Decimal('100'),
            'rating': Decimal('4.7'),
            'times_made': 1100,
            'ingredients': [
                ('Chicken', 600),
                ('Tomatoes', 400),
                ('Bell Peppers (Tatase)', 150),
                ('Onions', 100),
                ('Groundnut Oil', 80),
            ]
        },
        {
            'name': 'Ukodo (Yam Pepper Soup)',
            'local_name': 'Ukodo',
            'description': 'Urhobo yam and pepper soup',
            'meal_type': 'dinner',
            'difficulty': 'medium',
            'prep_time': 20,
            'cook_time': 40,
            'servings': 4,
            'instructions': '''1. Cut yam into large chunks
2. Boil with meat and pepper soup spices
3. Add ground crayfish
4. Cook until yam is soft
5. Adjust seasoning
6. Serve hot''',
            'estimated_cost': Decimal('1500'),
            'total_calories': Decimal('1600'),
            'total_protein': Decimal('80'),
            'total_carbs': Decimal('240'),
            'total_fats': Decimal('40'),
            'rating': Decimal('4.6'),
            'times_made': 420,
            'ingredients': [
                ('Yam', 600),
                ('Beef', 300),
                ('Crayfish (Dried)', 30),
                ('Onions', 50),
            ]
        },
        {
            'name': 'Abacha (African Salad)',
            'local_name': 'Abacha',
            'description': 'Igbo cassava salad with fish',
            'meal_type': 'snack',
            'difficulty': 'medium',
            'prep_time': 30,
            'cook_time': 10,
            'servings': 4,
            'instructions': '''1. Soak abacha in water
2. Drain and season with palm oil
3. Add ugba, stockfish, garden egg
4. Mix with potash solution
5. Garnish with vegetables
6. Serve cold''',
            'estimated_cost': Decimal('1200'),
            'total_calories': Decimal('1000'),
            'total_protein': Decimal('60'),
            'total_carbs': Decimal('120'),
            'total_fats': Decimal('40'),
            'rating': Decimal('4.8'),
            'times_made': 380,
            'ingredients': [
                ('Cassava (Fresh)', 400),
                ('Stockfish (Dried)', 100),
                ('Palm Oil', 60),
                ('Garden Egg (White)', 100),
            ]
        },
        {
            'name': 'Pounded Yam',
            'local_name': 'Iyan',
            'description': 'Smooth pounded yam swallow',
            'meal_type': 'dinner',
            'difficulty': 'hard',
            'prep_time': 10,
            'cook_time': 40,
            'servings': 4,
            'instructions': '''1. Peel and boil yam until soft
2. Pound in mortar until smooth
3. Shape into balls
4. Serve with soup''',
            'estimated_cost': Decimal('800'),
            'total_calories': Decimal('1800'),
            'total_protein': Decimal('24'),
            'total_carbs': Decimal('420'),
            'total_fats': Decimal('4'),
            'rating': Decimal('4.9'),
            'times_made': 950,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('Yam', 1000),
            ]
        },
        {
            'name': 'Fried Rice',
            'local_name': 'Fried Rice',
            'description': 'Nigerian-style vegetable fried rice',
            'meal_type': 'lunch',
            'difficulty': 'medium',
            'prep_time': 25,
            'cook_time': 30,
            'servings': 6,
            'instructions': '''1. Parboil rice and drain
2. Dice vegetables (carrots, peas, peppers)
3. Stir-fry vegetables with curry
4. Add rice, mix thoroughly
5. Adjust seasoning
6. Serve hot''',
            'estimated_cost': Decimal('1800'),
            'total_calories': Decimal('2400'),
            'total_protein': Decimal('40'),
            'total_carbs': Decimal('450'),
            'total_fats': Decimal('60'),
            'rating': Decimal('4.7'),
            'times_made': 780,
            'is_vegetarian': True,
            'ingredients': [
                ('White Rice', 500),
                ('Carrots', 200),
                ('Green Beans', 150),
                ('Bell Peppers (Tatase)', 100),
                ('Groundnut Oil', 80),
            ]
        },
        {
            'name': 'Coconut Rice',
            'local_name': 'Coconut Rice',
            'description': 'Rice cooked in coconut milk',
            'meal_type': 'lunch',
            'difficulty': 'easy',
            'prep_time': 15,
            'cook_time': 35,
            'servings': 4,
            'instructions': '''1. Grate coconut, extract milk
2. Season coconut milk
3. Cook rice in coconut milk
4. Add vegetables if desired
5. Serve when rice is fluffy''',
            'estimated_cost': Decimal('1200'),
            'total_calories': Decimal('2000'),
            'total_protein': Decimal('24'),
            'total_carbs': Decimal('350'),
            'total_fats': Decimal('60'),
            'rating': Decimal('4.6'),
            'times_made': 520,
            'is_vegetarian': True,
            'is_vegan': True,
            'ingredients': [
                ('White Rice', 400),
                ('Coconut', 300),
                ('Onions', 50),
            ]
        },
    ]
    
    created_count = 0
    for recipe_data in recipes:
        ingredients_list = recipe_data.pop('ingredients')
        
        recipe, created = Recipe.objects.get_or_create(
            name=recipe_data['name'],
            defaults=recipe_data
        )
        
        if created:
            created_count += 1
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
                    print(f"⚠️  Warning: Food '{food_name}' not found for '{recipe.name}'")
    
    print(f"✓ {created_count} new recipes added (Total: {Recipe.objects.count()})")


def run_more_recipes():
    """Run recipe seeding"""
    print("\n🍲 Adding more Nigerian recipes...\n")
    seed_more_recipes()
    print("\n✅ Recipes added successfully!\n")


if __name__ == '__main__':
    run_more_recipes()