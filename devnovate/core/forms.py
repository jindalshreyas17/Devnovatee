# core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Team, Sponsorship, Event, Project, ForumTopic, ForumReply, SupportTicket, Message
from django.utils import timezone
import os
from .models import ParticipantRegistration

class ParticipantRegistrationForm(forms.ModelForm):
    create_team = forms.ChoiceField(
        choices=[("Yes", "Yes"), ("No", "No")], 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ParticipantRegistration
        fields = ['name', 'email', 'event', 'create_team', 'role', 'experience',
                  'hackathon_experience', 'goal', 'team_status', 'communication']
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Choose a username',
            'autocomplete': 'username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Enter password',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Confirm password',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']
        widgets = {
            'role': forms.HiddenInput(attrs={'class': 'hidden'})
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'members']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter team name'
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            })
        }

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter team name (e.g., Team Alpha)'
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name=name).exists():
            raise forms.ValidationError("A team with this name already exists.")
        return name

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'team', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter project title (e.g., AI Chatbot)'
            }),
            'team': forms.Select(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Select a team'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter project description',
                'rows': 3
            })
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Project.objects.filter(title=title).exists():
            raise forms.ValidationError("A project with this title already exists.")
        return title

class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['event', 'amount', 'tier']
        widgets = {
            'event': forms.Select(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Select an event'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter sponsorship amount'
            }),
            'tier': forms.Select(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Select sponsorship tier'
            })
        }

class SponsorProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company_name', 'contact_info', 'logo']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter company name'
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter contact information'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'w-full p-2',
                'placeholder': 'Upload company logo'
            })
        }

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            valid_extensions = ['.png', '.jpg', '.jpeg']
            ext = os.path.splitext(logo.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Only PNG, JPG, and JPEG files are allowed.")
            max_size = 2 * 1024 * 1024
            if logo.size > max_size:
                raise forms.ValidationError("File size must be less than 2MB.")
        return logo

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'is_online', 'is_offline', 'is_hybrid', 'status', 'description']
        widgets = {
    'name': forms.TextInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Enter event name (e.g., Hackathon 2025)'
    }),
    'date': forms.DateTimeInput(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'YYYY-MM-DD HH:MM (e.g., 2025-05-10 10:00)',
        'type': 'datetime-local'
    }),
    'is_online': forms.CheckboxInput(attrs={'class': 'mr-2'}),  # ✅ Added widget
    'is_offline': forms.CheckboxInput(attrs={'class': 'mr-2'}),  # ✅ Added widget
    'is_hybrid': forms.CheckboxInput(attrs={'class': 'mr-2'}),  # ✅ Added widget
    'description': forms.Textarea(attrs={
        'class': 'w-full p-2 border rounded',
        'placeholder': 'Provide event details'
    })
}


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Event.objects.filter(name=name).exists():
            raise forms.ValidationError("An event with this name already exists.")
        return name

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError("Event date cannot be in the past.")
        return date

class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter topic title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Describe your topic or question',
                'rows': 4
            })
        }

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Write your reply',
                'rows': 3
            })
        }

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter ticket subject'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Describe your issue',
                'rows': 4
            })
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.Select(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Select a sponsor'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Write your message',
                'rows': 3
            })
        }
