from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse
from myapp.forms import  GoalForm
from django.shortcuts import redirect
import openai
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from openai import ChatCompletion
from googleapiclient.discovery import build
import requests
from django.contrib import messages

from datetime import datetime
import calendar
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import YearlyGoal, MonthlyGoal, WeeklyGoal, LongTermGoal, DailyGoal , Profile, User, Goal
from django.utils import timezone
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random
import uuid






def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')  # Redirect to the index page after login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})





prompts = {
    "Personal Development": "Give me an example of a personal development goal.",
    "Career Advancement": "Give me an example of a career advancement goal.",
    "Health and Wellness": "Give me an example of a health and wellness goal.",
    "Financial Planning": "Give me an example of a financial planning goal."
}

# Function to generate an example using chat completion
def generate_example(promp):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or any other chat model you prefer
        messages=[
            {"role": "system", "content": "You are an assistant that provides specific goal examples."},
            {"role": "user", "content": promp}
        ],
        max_tokens=1000
    )
    example = response.choices[0].message['content'].strip()
    return example






def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            # Create a profile for the user
            user = User.objects.get(id=user.id)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in.')
            login(request, user)  # Ensure this is the correct login function
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})








def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    yearly_goals = YearlyGoal.objects.filter(profile=profile)

    return render(request, 'profile.html', {
        'profile': profile,
        'yearly_goals': yearly_goals,
    })
    


@login_required
def index(request):
    if request.method == 'POST':
        # If the request method is POST, process the form data
        form = GoalForm(request.POST)
        if form.is_valid():
            # If the form is valid, extract the goal_text from the form data
            goal_text = form.cleaned_data['goal']
            
            # Create a new Goal instance with the extracted goal_text
            goal = Goal.objects.create(goal_text=goal_text)
            
            # Redirect to the generate_long_term_goal page with the newly created goal's ID
            return redirect(reverse('generate_long_term_goal', kwargs={'id': goal.id}))
    else:
        # If the request method is GET (or any other), initialize a new instance of the GoalForm
        form = GoalForm()
    
    # Render the index.html template with the form
    return render(request, 'index.html', {'form': form})






def generate_long_term_goal(request, id):
    # Get the goal instance using the provided ID
    goal = get_object_or_404(Goal, pk=id)

    # Extract the goal text from the goal instance
    prompt = goal.goal_text

    if not prompt:
        # Handle the case where prompt is not provided or is empty
        return redirect('index')  # Redirect to the index page

    # Generate long-term goal using OpenAI ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000
    )

    # Extract the generated goal from the response
    generated_goal = response.choices[0].message['content'].strip()

    # Render the goal_selection.html template with the generated goal
    return render(request, 'goal_selection.html', {'goal': generated_goal, 'id':id}, )




def generate_long_term(request, id):
    if request.method == 'POST':
        # Check if the request body contains JSON data
        try:
            selected_option = request.POST.dict()  # Convert POST data to a dictionary
        except AttributeError:
            return JsonResponse({'error': 'Invalid request. Please provide JSON data.'}, status=400)
        
        # Extract the selected option and tier from the dictionary
        option = selected_option.get('selected_option')
        tier = selected_option.get('selected_tier')
        
        if tier:
            # Construct a prompt based on the selected tier and option
            if tier == "low":
                prompt = f"Generate a long-term goal option that can be achieved within 1-3 years based on the following input: {option}"
            elif tier == "medium":
                prompt = f"Generate a long-term goal option that can be achieved within 3-5 years based on the following input: {option}"
            elif tier == "high":
                prompt = f"Generate a long-term goal option that can be achieved within 5-10 years based on the following input: {option}"
            else:
                return JsonResponse({'error': 'Invalid tier selection. Please choose a valid option.'}, status=400)
            
            # Use OpenAI's ChatCompletion API to generate the long-term goal
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ],
                max_tokens=1000
            )
            long_term_goals = response.choices[0].message['content'].strip()
        else:
            # If no tier is specified, generate a long-term goal based only on the selected option
            # Here, you would implement your logic for generating a long-term goal based on the selected option
            # For demonstration purposes, I'll just return a placeholder string
            long_term_goals = f"This is a long-term goal generated based on the selected option: {option}"
        
        # Pass the generated long-term goal to a template for rendering
        return render(request, 'long_term_goal.html', {'long_term_goals': long_term_goals, 'id':id})

      # Redirect to the index page if accessed directly without a POST request
    return redirect('index')





def generate_goal_options(selected_goal, selected_tier):
    # Define different prompts emphasizing different aspects or dimensions of the user's input
    prompts = [
        f"What are some career-oriented goals that align with '{selected_goal}'?",
        f"Generate personal development goals related to '{selected_goal}'",
        f"Propose social impact goals inspired by '{selected_goal}'"
    ]

    goal_options = []

    # Generate goal options for each prompt
    for prompt in prompts:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Using the chat model
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            n=1,  # Generate 1 option per prompt
            temperature=0.7,  # Control the diversity of generated responses
            top_p=1.0,  # Control the diversity of generated responses
            frequency_penalty=0.0,  # Control the diversity of generated responses
            presence_penalty=0.0,  # Control the diversity of generated responses
        )

        # Extract and append generated options
        goal_options.extend([choice["message"]["content"].strip() for choice in response.choices])

    return goal_options









def generate_options(request, id):
    if request.method == 'POST':
        selected_goal = request.POST.get('selected_goal')
        selected_tier = request.POST.get('selected_tier')
        
        # Generate diverse goal options based on the selected goal and tier
        options = generate_goal_options(selected_goal, selected_tier)
        selected_option = request.POST.get('selected_option')
        
        # Render the option selection page with the generated options
        return render(request, 'option_selection.html', {'options': options, 'selected_option': selected_option, 'id': id} )
    # Redirect to the index page if accessed directly without a POST request
    return redirect('index')



  
  

@login_required
def generate_long_term_goals(request):
    if request.method == 'POST':
        options = request.POST.get('option')

        if not options:
            return HttpResponseBadRequest("No option provided")
        
        prompt = f"Long-term goal based on option '{options}'"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            long_term_goal_text = response.choices[0].message['content'].strip()

            if not long_term_goal_text:
                return HttpResponseBadRequest("Failed to generate a valid long-term goal")

            # Check if the user has an associated profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            if created:
                print("New profile created:", profile)

            # Save the LongTermGoal with the associated profile
            long_term_goal = LongTermGoal.objects.create(
                profile=profile,
                description=long_term_goal_text
            )

            print("LongTermGoal saved successfully:", long_term_goal)

            # Create the YearlyGoal associated with the long-term goal
            yearly_goal = YearlyGoal.objects.create(
                profile=profile,
                title=long_term_goal_text,  # Use the same title as the long-term goal for now
                description="",  # You can leave this blank or provide a default value
                year=timezone.now().year
            )

            print("YearlyGoal saved successfully:", yearly_goal)

            # Redirect the user to the generate_year_plan page with the yearly_goal ID
            return redirect('generate_year_plan', id=id)

        except Exception as e:
            print(f"Error generating goals: {e}")
            return HttpResponseBadRequest("Failed to generate goals")
    
    return HttpResponseBadRequest("Invalid request method")


def generate_year_plan(request, id=None):
    if request.method == 'POST':
        long_term_goal = request.POST.get('long_term_goal')
        
        # Debugging: Print received long_term_goal
        print("Received long_term_goal:", long_term_goal)

        if not long_term_goal:
            return HttpResponseBadRequest("Invalid long-term goal")

        year_plan_prompt = f"What are the steps to achieve the long-term goal '{long_term_goal}' within a year?"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": year_plan_prompt}],
                max_tokens=1000
            )
            year_plan = response.choices[0].message['content'].strip()

            if not year_plan:
                return HttpResponseBadRequest("Failed to generate a valid year plan")

            # Save the Yearly Goal
            profile = request.user.profile
            year = timezone.now().year

            # Create a new YearlyGoal
            yearly_goal = YearlyGoal.objects.create(
                profile=profile,
                year=year,
                title=long_term_goal,
                description=year_plan
            )

            print("YearlyGoal created successfully:", yearly_goal)

            # Render the template with the generated year plan
            return render(request, 'year_plan.html', {'yearly_goal': yearly_goal, 'year_plan': year_plan, 'id': id})

        except Exception as e:
            print(f"Error generating year plan: {e}")
            return HttpResponseBadRequest("Failed to generate year plan")

    # Handle GET requests
    elif request.method == 'GET':
        if id is None:
            return render(request, 'create_yearly_goal.html')
        else:
            yearly_goal = get_object_or_404(YearlyGoal, pk=id)
            return render(request, 'year_plan.html', {'yearly_goal': yearly_goal})

    return HttpResponseBadRequest("Invalid request method")

  


def generate_month_to_month_plans_from_year_plan(year_plan):
    """
    Generates month-to-month plans from a year plan using OpenAI GPT-4.
    """
    month_to_month_plans = []
    for month in range(1, 13):
        month_prompt = f"What are the steps to achieve the long-term goal '{year_plan}' within month {month}?"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": month_prompt}],
            max_tokens=700
        )
        month_plan = response.choices[0].message['content'].strip()
        month_to_month_plans.append((month, month_plan))
    return month_to_month_plans

def generate_month_to_month_plans_view(request, id):
    try:
        year_plan = request.POST.get('year_plan')
        yearly_goal_id = request.POST.get('yearly_goal')

        # Debugging: Print received year_plan and yearly_goal_id
        print("Received year_plan:", year_plan)
        print("Received yearly_goal_id:", yearly_goal_id)

        if not year_plan or not yearly_goal_id:
            # Debugging: Print which part is missing
            if not year_plan:
                print("Year plan is missing")
            if not yearly_goal_id:
                print("Yearly goal ID is missing")
            
            return HttpResponseBadRequest("Missing year plan or yearly goal")

        # Retrieve the YearlyGoal object
        yearly_goal = YearlyGoal.objects.get(id=yearly_goal_id)

        # Generate month-to-month plans from the year plan
        month_to_month_plans = generate_month_to_month_plans_from_year_plan(year_plan)
        current_month = timezone.now().month
        month_names = [calendar.month_name[(current_month + i - 1) % 12 + 1] for i in range(12)]

        month_to_month_plans_named = []
        for i, (month_name, month_plan) in enumerate(zip(month_names, month_to_month_plans)):
            # Check if a MonthlyGoal already exists for this month
            monthly_goal, created = MonthlyGoal.objects.get_or_create(
                yearly_goal=yearly_goal,
                month=(current_month + i - 1) % 12 + 1,
                defaults={'description': month_plan[1]}
            )
            month_to_month_plans_named.append((month_name, monthly_goal.id, monthly_goal.description))
        # Store the month-to-month plans and year plan in the session
        request.session['month_to_month_plans'] = month_to_month_plans_named
        request.session['year_plan'] = year_plan  # Store the year plan for reference

        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        return render(request, 'month.html', {
            'month_to_month_plans': month_to_month_plans_named,
            'timestamp': timestamp,
            'id': id
        })

    
    except YearlyGoal.DoesNotExist:
        return JsonResponse({'error': 'Yearly goal not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
    
def generate_week_to_week_plans_view(request, id):
    try:
        # Retrieve month_to_month_plans from the session
        month_to_month_plans = request.session.get('month_to_month_plans')

        # Debugging: Print the content of month_to_month_plans
        print("Month to month plans:", month_to_month_plans)

        # Check if month_to_month_plans is present
        if not month_to_month_plans:
            return redirect('generate_month_to_month_plans_view')

        week_to_week_plans_by_month = []

        # Iterate over each month plan
        for i, month_plan in enumerate(month_to_month_plans):
            # Debugging: Print the content of the current month_plan
            print("Processing month_plan:", month_plan)

            # Ensure the month_plan is a tuple or list with exactly three values
            if not isinstance(month_plan, (tuple, list)) or len(month_plan) != 3:
                raise ValueError(f"Invalid month_plan format: {month_plan}")

            month_name, month_plan_id, month_plan_description = month_plan

            # Ensure month_plan_id is a valid number
            if not isinstance(month_plan_id, int):
                raise ValueError(f"Invalid month_plan_id: {month_plan_id}")

            # Get the MonthlyGoal instance using the ID
            monthly_goal = MonthlyGoal.objects.get(id=month_plan_id)

            # Generate week-to-week plans
            week_plans = generate_week_to_week_plans_from_month_plan(monthly_goal, i * 4 + 1)
            week_to_week_plans_by_month.append((month_name, week_plans))

        print("Week to week plans by month:", week_to_week_plans_by_month)

        return render(request, 'week.html', {'week_to_week_plans_by_month': week_to_week_plans_by_month, 'id': id})
    except MonthlyGoal.DoesNotExist:
        return JsonResponse({'error': 'Monthly goal not found'}, status=404)
    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    
    
    
    
    
    
    
    
    
    
import time

def generate_week_to_week_plans_from_month_plan(monthly_goal, start_week, max_retries=3, retry_delay=5):
    """
    Generates week-to-week plans from a single month plan and saves them as WeeklyGoal instances.

   
    """
    if not isinstance(monthly_goal, MonthlyGoal):
        raise ValueError("The monthly_goal parameter must be a MonthlyGoal instance")

    week_to_week_plans = []
    month_plan = monthly_goal.description
    month_name = calendar.month_name[monthly_goal.month]  # Assuming 'month' is an integer field

    for week in range(start_week, start_week + 4):  # Assuming 4 weeks per month
        week_prompt = f"What are the steps to achieve the month goal '{month_plan}' for {month_name} in week {week - start_week + 1}?"
        print(f"Generating plan for: {week_prompt}")  # Debugging: Print the prompt

        retries = 0
        while retries < max_retries:
            try:
                response = ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": week_prompt}],
                    max_tokens=1000
                )
                week_plan = response.choices[0].message['content'].strip()

                if not week_plan:
                    raise ValueError("Received empty week plan from OpenAI API")

                # Check if a WeeklyGoal already exists for the given monthly_goal and week
                weekly_goal, created = WeeklyGoal.objects.update_or_create(
                    monthly_goal=monthly_goal,
                    week=week,
                    defaults={'description': week_plan}
                )

                if not weekly_goal.id:
                    raise ValueError("Failed to save the weekly goal to the database")

                week_to_week_plans.append((f"Week {week - start_week + 1}", week_plan))

                # Debugging: Confirm that the weekly goal was saved
                print(f"{'Created' if created else 'Updated'} weekly goal: {weekly_goal.description}")
                break
            except Exception as e:
                if "connection was forcibly closed by the remote host" in str(e):
                    retries += 1
                    print(f"Connection error: {str(e)}. Retrying {retries}/{max_retries}...")
                    time.sleep(retry_delay)
                else:
                    print(f"Error generating or saving week plan for week {week - start_week + 1}: {str(e)}")  # Debugging: Print the error
                    raise

    return week_to_week_plans




def generate_daily_goal_view(request, id):
    user = request.user  # Assuming user is authenticated
    week_plan_description = request.POST.get('week_plan_description')
    current_date = datetime.now().date()

    try:
        profile = Profile.objects.get(user=user,)
        new_daily_goal = generate_daily_goal_from_week_plan(profile, week_plan_description, current_date)
        return render(request, 'daily_goal.html', {'daily_goal': new_daily_goal})
    except Profile.DoesNotExist:
        return render(request, 'daily_goal.html', {'error': 'Profile does not exist for the current user.'})
    except Exception as e:
        return render(request, 'daily_goal.html', {'error': str(e), 'id':id} )
  
                
from datetime import datetime

def generate_daily_goal_from_week_plan(profile, week_plan_description, current_date):
    try:
        # Retrieve all yearly goals for the current year
        yearly_goals = YearlyGoal.objects.filter(profile=profile, year=current_date.year)

        # If there are multiple yearly goals, select the most recent one
        if yearly_goals.exists():
            yearly_goal = yearly_goals.latest('created_at')  # Assuming there's a 'created_at' field
        else:
            # If no yearly goal exists, create a new one
            yearly_goal = YearlyGoal.objects.create(profile=profile, year=current_date.year)

        # Ensure the current month's goal exists or create a new one
        monthly_goal, monthly_goal_created = MonthlyGoal.objects.get_or_create(
            yearly_goal=yearly_goal,
            month=current_date.month,
            defaults={}
        )

        week_number = current_date.isocalendar()[1]

        # Ensure the current week's goal exists or create a new one
        weekly_goal, weekly_goal_created = WeeklyGoal.objects.get_or_create(
            monthly_goal=monthly_goal,
            week=week_number,
            defaults={}
        )

        # Find existing daily goals for the current week
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)
        weekly_goals = DailyGoal.objects.filter(
            profile=profile,
            weekly_goal=weekly_goal,
            date__range=[week_start, week_end]
        )

        # Get descriptions of existing daily goals for uniqueness check
        existing_descriptions = set(goal.description for goal in weekly_goals)

        is_unique = False
        new_goal_description = ""
        attempts = 0
        max_attempts = 5

        while not is_unique and attempts < max_attempts:
            attempts += 1

            day_prompt = f"What are the steps to achieve the week goal '{week_plan_description}' on {current_date.strftime('%A')}?"
            response = ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": day_prompt}],
                max_tokens=1000
            )
            day_plan = response.choices[0].message['content'].strip()

            # Placeholder for generating additional content
            additional_content = "Additional content related to the week plan description."

            new_goal_description = f"{day_plan} {additional_content}"

            # Check uniqueness of the new goal description
            is_unique = new_goal_description not in existing_descriptions

        if not is_unique:
            raise Exception("Unable to generate a unique goal after several attempts.")

        # Create the daily goal
        daily_goal = DailyGoal.objects.create(
            profile=profile,
            weekly_goal=weekly_goal,
            title=f"Daily Goal for {current_date.strftime('%A')}",
            description=new_goal_description,
            date=current_date,
            monthly_goal=monthly_goal,  # Assign the monthly goal here
            yearly_goal=yearly_goal  # Assign the yearly goal here
        )
        
        # Return the created daily goal
        return daily_goal
    except Exception as e:
        raise Exception(f"Error generating daily goal: {str(e)}")



from django.http import HttpResponseBadRequest
