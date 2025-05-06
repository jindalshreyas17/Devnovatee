from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models  
from .models import Event,  ParticipantRegistration
from .forms import ParticipantRegistrationForm

from .forms import (
    UserRegistrationForm, ProfileForm, SponsorshipForm, SponsorProfileForm, EventForm,
    TeamCreationForm, ProjectCreationForm, ForumTopicForm, ForumReplyForm, SupportTicketForm, MessageForm
)
from .models import Profile, Sponsorship, Project, Event, Team, ForumTopic, ForumReply, SupportTicket, Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'profile'):
            login(request, user)
            if user.profile.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.profile.role == 'SPONSOR':
                return redirect('sponsor_front')
            else:
                return redirect('participant_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    role = request.GET.get('role', 'PARTICIPANT')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.create(user=user, role=role)
            login(request, user)
            if role == 'ADMIN':
                return redirect('admin_dashboard')
            elif role == 'SPONSOR':
                return redirect('sponsor_front')
            else:
                return redirect('participant_dashboard')
        else:
            messages.error(request, 'Error in form submission. Please try again.')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm(initial={'role': role})
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'role': role
    })

@login_required
def admin_dashboard(request):
    participants = Profile.objects.filter(role='PARTICIPANT')
    sponsors = Profile.objects.filter(role='SPONSOR')
    return render(request, 'admin_dashboard.html', {
        'profiles': participants,
        'sponsors': sponsors,
        'role': 'ADMIN'
    })

@login_required
def sponsor_front(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'SPONSOR':
        return redirect('index')
    
    # Fetch dynamic data
    sponsorships = Sponsorship.objects.filter(sponsor=request.user.profile)
    projects = Project.objects.all()
    events = Event.objects.all()
    teams = Team.objects.all()
    
    # Counts for Sponsor Status
    events_count = sponsorships.count()
    projects_count = projects.count()
    
    # Forms
    sponsorship_form = SponsorshipForm()
    event_form = EventForm()
    team_form = TeamCreationForm()
    project_form = ProjectCreationForm()
    profile_form = SponsorProfileForm(instance=request.user.profile)
    
    return render(request, 'sponsor_front.html', {
        'sponsorships': sponsorships,
        'projects': projects,
        'events': events,
        'teams': teams,
        'events_count': events_count,
        'projects_count': projects_count,
        'sponsorship_form': sponsorship_form,
        'event_form': event_form,
        'team_form': team_form,
        'project_form': project_form,
        'profile_form': profile_form,
        'role': 'SPONSOR'
    })

@login_required
def create_sponsorship(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'SPONSOR':
        return redirect('index')
    
    if request.method == 'POST':
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sponsorship = form.save(commit=False)
            sponsorship.sponsor = request.user.profile
            sponsorship.save()
            messages.success(request, 'Sponsorship created successfully!')
            return redirect('sponsor_front')
        else:
            messages.error(request, 'Error creating sponsorship. Please check the form.')
    return redirect('sponsor_front')

@login_required
def create_event(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'SPONSOR':
        return redirect('index')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('sponsor_front')
        else:
            messages.error(request, 'Error creating event. Please check the form.')
    return redirect('sponsor_front')

@login_required
def update_sponsor_profile(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'SPONSOR':
        return redirect('index')

    if request.method == 'POST':
        form = SponsorProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('sponsor_front')
        else:
            messages.error(request, 'Error updating profile. Please check the form.')
    
    profile_form = SponsorProfileForm(instance=request.user.profile)
    
    return render(request, 'sponsor_front.html', {
        'profile_form': profile_form,
        'role': 'SPONSOR'
    })


@login_required
def community_forums(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'SPONSOR':
        return redirect('index')
    
    topics = ForumTopic.objects.all().order_by('-created_at')
    topic_form = ForumTopicForm()
    reply_form = ForumReplyForm()
    
    return render(request, 'forum.html', {
        'topics': topics,
        'topic_form': topic_form,
        'reply_form': reply_form
    })

@login_required
def create_forum_topic(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user.profile
            topic.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('community_forums')
        else:
            messages.error(request, 'Error creating topic. Please check the form.')
    return redirect('community_forums')

@login_required
def create_forum_reply(request, topic_id):
    topic = ForumTopic.objects.get(id=topic_id)
    if request.method == 'POST':
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user.profile
            reply.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('community_forums')
    return redirect('community_forums')

@login_required
def support(request):
    tickets = SupportTicket.objects.filter(user=request.user.profile).order_by('-created_at')
    ticket_form = SupportTicketForm()
    return render(request, 'support.html', {'tickets': tickets, 'ticket_form': ticket_form})

@login_required
def submit_support_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user.profile
            ticket.save()
            messages.success(request, 'Support ticket submitted successfully!')
            return redirect('support')
    return redirect('support')

@login_required
def networking(request):
    sponsors = Profile.objects.filter(role='SPONSOR').exclude(user=request.user)
    messages_list = Message.objects.filter(models.Q(sender=request.user.profile) | models.Q(receiver=request.user.profile)).order_by('-sent_at')
    message_form = MessageForm()
    return render(request, 'networking.html', {'sponsors': sponsors, 'messages': messages_list, 'message_form': message_form})

@login_required
def send_message(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'SPONSOR':
        return redirect('index')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('sponsor_networking')  
    return redirect('sponsor_networking')


def about(request):
    return render(request, 'about.html')

def FAQ(request):
    return render(request, 'FAQ.html')

def Contact(request):
    return render(request, 'Contact.html')

@login_required
def participant_dashboard(request):
    total_participants = Profile.objects.filter(role='PARTICIPANT').count()
    active_events = Event.objects.filter(status="active")[:6]
    event_slots = list(active_events) + ["Coming Soon"] * (6 - len(active_events))
    return render(request, 'participant_dashboard.html', {'total_participants': total_participants, 'event_slots': event_slots, 'role': 'PARTICIPANT'})

@login_required
@csrf_exempt  # Allows AJAX requests
def formregisteration(request):
    if request.method == 'POST':
        print("Incoming POST Data:", request.POST)  # ✅ Debugging
        
        form = ParticipantRegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user
            participant.save()
            return JsonResponse({"success": True, "message": "Registration successful!"})
        else:
            print("Form Errors:", form.errors)  # ✅ Debug errors
            return JsonResponse({"success": False, "message": "Invalid form data", "errors": form.errors.as_json()}, status=400)

    events = Event.objects.all()
    form = ParticipantRegistrationForm()
    return render(request, 'formregisteration.html', {'form': form, 'events': events})
