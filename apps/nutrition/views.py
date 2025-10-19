# views.py - API Views

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta

# Import all serializers
from .serializers import (
    UserProfileSerializer,
    FoodSerializer,
    RecipeListSerializer,
    RecipeDetailSerializer,
    MealPlanSerializer,
    UserMealLogSerializer,
    HealthTipSerializer
)

# Import models
from .models import (
    User, 
    Food, 
    Recipe, 
    RecipeIngredient, 
    MealPlan, 
    UserMealLog, 
    HealthTip, 
    FoodCategory
)

# Import recommendation engine
from .recommendation_engine import MealRecommendationEngine


# Now the ViewSets start here...
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    User profile management
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user's profile"""
        serializer = self.get_serializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Browse foods database
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Food.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name=category)
        
        # Filter by dietary preferences
        if self.request.query_params.get('vegetarian') == 'true':
            queryset = queryset.filter(is_vegetarian=True)
        if self.request.query_params.get('vegan') == 'true':
            queryset = queryset.filter(is_vegan=True)
        
        # Filter by health conditions
        if self.request.query_params.get('diabetes_friendly') == 'true':
            queryset = queryset.filter(suitable_for_diabetes=True)
        if self.request.query_params.get('hypertension_friendly') == 'true':
            queryset = queryset.filter(suitable_for_hypertension=True)
        
        # Filter by season
        if self.request.query_params.get('seasonal') == 'true':
            current_month = timezone.now().strftime('%b')
            queryset = queryset.filter(
                is_seasonal=True,
                available_months__icontains=current_month
            )
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('name')
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all food categories"""
        categories = FoodCategory.objects.all()
        return Response([
            {'id': cat.id, 'name': cat.name, 'description': cat.description}
            for cat in categories
        ])
    
    @action(detail=False, methods=['get'])
    def seasonal(self, request):
        """Get seasonal foods for current month"""
        current_month = timezone.now().strftime('%b')
        seasonal_foods = Food.objects.filter(
            is_seasonal=True,
            available_months__icontains=current_month
        )
        serializer = self.get_serializer(seasonal_foods, many=True)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Browse recipes
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return RecipeListSerializer
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.user
        
        # Filter by meal type
        meal_type = self.request.query_params.get('meal_type', None)
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by dietary preferences
        if user.is_vegetarian:
            queryset = queryset.filter(is_vegetarian=True)
        if user.is_vegan:
            queryset = queryset.filter(is_vegan=True)
        if user.is_halal:
            queryset = queryset.filter(is_halal=True)
        
        # Filter by max cost
        max_cost = self.request.query_params.get('max_cost', None)
        if max_cost:
            queryset = queryset.filter(estimated_cost__lte=max_cost)
        
        # Filter by max prep time
        max_time = self.request.query_params.get('max_time', None)
        if max_time:
            total_time = int(max_time)
            queryset = queryset.extra(
                where=[f"prep_time + cook_time <= {total_time}"]
            )
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Order by
        order_by = self.request.query_params.get('order_by', '-rating')
        queryset = queryset.order_by(order_by)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular recipes"""
        recipes = Recipe.objects.order_by('-times_made', '-rating')[:10]
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def quick(self, request):
        """Get quick recipes (under 30 minutes total)"""
        recipes = Recipe.objects.extra(
            where=["prep_time + cook_time <= 30"]
        ).order_by('-rating')[:10]
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def budget_friendly(self, request):
        """Get affordable recipes"""
        recipes = Recipe.objects.order_by('estimated_cost')[:10]
        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate a recipe"""
        recipe = self.get_object()
        rating = request.data.get('rating')
        
        if not rating or not (0 <= float(rating) <= 5):
            return Response(
                {'error': 'Rating must be between 0 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simple rating update (in production, track individual user ratings)
        recipe.rating = (recipe.rating * recipe.times_made + float(rating)) / (recipe.times_made + 1)
        recipe.times_made += 1
        recipe.save()
        
        return Response({'success': True, 'new_rating': recipe.rating})


class MealPlanViewSet(viewsets.ModelViewSet):
    """
    Manage meal plans
    """
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        meal_plan = serializer.save(user=self.request.user)
        meal_plan.calculate_totals()
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's meal plan"""
        today = timezone.now().date()
        try:
            meal_plan = MealPlan.objects.get(user=request.user, date=today)
            serializer = self.get_serializer(meal_plan)
            return Response(serializer.data)
        except MealPlan.DoesNotExist:
            return Response(
                {'message': 'No meal plan for today. Generate one using /generate/'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def week(self, request):
        """Get this week's meal plans"""
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)
        
        meal_plans = MealPlan.objects.filter(
            user=request.user,
            date__gte=week_start,
            date__lt=week_end
        ).order_by('date')
        
        serializer = self.get_serializer(meal_plans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate AI meal plan for a specific date"""
        target_date = request.data.get('date')
        
        if target_date:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        else:
            target_date = timezone.now().date()
        
        # Check if meal plan already exists
        existing_plan = MealPlan.objects.filter(
            user=request.user,
            date=target_date
        ).first()
        
        if existing_plan and not request.data.get('force_regenerate'):
            return Response(
                {'message': 'Meal plan already exists for this date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate recommendations using AI engine
        engine = MealRecommendationEngine(request.user)
        recommendations = engine.generate_daily_meal_plan(target_date)
        
        # Create or update meal plan
        if existing_plan:
            meal_plan = existing_plan
        else:
            meal_plan = MealPlan(user=request.user, date=target_date)
        
        # Assign top recommendations
        if recommendations['breakfast']:
            meal_plan.breakfast = recommendations['breakfast'][0]['recipe']
        if recommendations['lunch']:
            meal_plan.lunch = recommendations['lunch'][0]['recipe']
        if recommendations['dinner']:
            meal_plan.dinner = recommendations['dinner'][0]['recipe']
        
        meal_plan.save()
        
        # Add snacks (many-to-many)
        if recommendations['snacks']:
            meal_plan.snacks.set([recommendations['snacks'][0]['recipe']])
        
        meal_plan.calculate_totals()
        
        serializer = self.get_serializer(meal_plan)
        return Response({
            'meal_plan': serializer.data,
            'all_recommendations': {
                'breakfast': [
                    {
                        'recipe': RecipeListSerializer(r['recipe']).data,
                        'match_percentage': r['match_percentage']
                    }
                    for r in recommendations['breakfast']
                ],
                'lunch': [
                    {
                        'recipe': RecipeListSerializer(r['recipe']).data,
                        'match_percentage': r['match_percentage']
                    }
                    for r in recommendations['lunch']
                ],
                'dinner': [
                    {
                        'recipe': RecipeListSerializer(r['recipe']).data,
                        'match_percentage': r['match_percentage']
                    }
                    for r in recommendations['dinner']
                ],
                'snacks': [
                    {
                        'recipe': RecipeListSerializer(r['recipe']).data,
                        'match_percentage': r['match_percentage']
                    }
                    for r in recommendations['snacks']
                ],
            }
        })
    
    @action(detail=True, methods=['post'])
    def mark_followed(self, request, pk=None):
        """Mark a meal plan as followed"""
        meal_plan = self.get_object()
        meal_plan.is_followed = True
        meal_plan.save()
        return Response({'success': True})


class MealLogViewSet(viewsets.ModelViewSet):
    """
    Track actual meals eaten
    """
    serializer_class = UserMealLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = UserMealLog.objects.filter(user=self.request.user)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date', '-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's meal logs"""
        today = timezone.now().date()
        logs = UserMealLog.objects.filter(user=request.user, date=today)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get meal logging statistics"""
        days = int(request.query_params.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        
        logs = UserMealLog.objects.filter(
            user=request.user,
            date__gte=start_date
        )
        
        total_logs = logs.count()
        total_calories = sum(
            log.recipe.calories_per_serving() if log.recipe else 0
            for log in logs
        )
        
        return Response({
            'period_days': days,
            'total_meals_logged': total_logs,
            'total_calories': total_calories,
            'average_meals_per_day': round(total_logs / days, 1),
            'average_calories_per_day': round(total_calories / days, 0)
        })


class RecommendationViewSet(viewsets.ViewSet):
    """
    AI-powered recommendations
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def for_you(self, request):
        """Get personalized recipe recommendations"""
        engine = MealRecommendationEngine(request.user)
        meal_type = request.query_params.get('meal_type', 'lunch')
        
        # Calculate targets
        daily_calories = request.user.calculate_daily_calories()
        calorie_distribution = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'dinner': 0.30,
            'snack': 0.10
        }
        
        target_calories = daily_calories * calorie_distribution.get(meal_type, 0.35)
        budget = request.user.daily_budget or 3000
        budget_per_meal = budget * calorie_distribution.get(meal_type, 0.35)
        
        recommendations = engine.recommend_meal(meal_type, target_calories, budget_per_meal)
        
        return Response({
            'meal_type': meal_type,
            'target_calories': target_calories,
            'budget': float(budget_per_meal),
            'recommendations': [
                {
                    'recipe': RecipeListSerializer(r['recipe']).data,
                    'match_percentage': r['match_percentage'],
                    'calories': r['calories_per_serving'],
                    'cost': float(r['cost_per_serving'])
                }
                for r in recommendations
            ]
        })
    
    @action(detail=False, methods=['get'])
    def seasonal(self, request):
        """Get seasonal recommendations"""
        engine = MealRecommendationEngine(request.user)
        seasonal_recipes = engine.get_seasonal_recommendations()
        serializer = RecipeListSerializer(seasonal_recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def grocery_list(self, request):
        """Generate grocery list for the week"""
        days = int(request.query_params.get('days', 7))
        engine = MealRecommendationEngine(request.user)
        grocery_list = engine.suggest_grocery_list(days)
        return Response(grocery_list)
    
    @action(detail=False, methods=['get'])
    def nutritional_gaps(self, request):
        """Analyze nutritional gaps"""
        engine = MealRecommendationEngine(request.user)
        gaps = engine.analyze_nutritional_gaps()
        
        return Response({
            'gaps': [
                {
                    'nutrient': gap['nutrient'],
                    'deficit': gap['deficit'],
                    'recommended_foods': FoodSerializer(gap['recommendation'], many=True).data
                }
                for gap in gaps
            ]
        })


class HealthTipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Health and nutrition tips
    """
    queryset = HealthTip.objects.all()
    serializer_class = HealthTipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = HealthTip.objects.all()
        user = self.request.user
        
        # Filter by relevance to user
        if user.has_diabetes:
            queryset = queryset.filter(relevant_for_diabetes=True)
        elif user.has_hypertension:
            queryset = queryset.filter(relevant_for_hypertension=True)
        elif user.health_goal == 'lose_weight':
            queryset = queryset.filter(relevant_for_weight_loss=True)
        
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def daily_tip(self, request):
        """Get a random daily tip"""
        import random
        tips = list(self.get_queryset())
        if tips:
            tip = random.choice(tips)
            serializer = self.get_serializer(tip)
            return Response(serializer.data)
        return Response({'message': 'No tips available'}, status=status.HTTP_404_NOT_FOUND)