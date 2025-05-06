from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# -------------------- Profile Model --------------------

class Profile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('PARTICIPANT', 'Participant'),
        ('SPONSOR', 'Sponsor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PARTICIPANT')
    company_name = models.CharField(max_length=100, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# -------------------- Team Model --------------------

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams', blank=True)

    def __str__(self):
        return self.name

# -------------------- Event Model --------------------

class Event(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    is_online = models.BooleanField(default=False)
    is_offline = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    time_remaining = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

# -------------------- Participant Registration Model --------------------

class ParticipantRegistration(models.Model):
    TEAM_STATUS_CHOICES = [
        ("already_have", "Already Have"),
        ("need_matching", "Need Matching"),
    ]
    COMMUNICATION_CHOICES = [
        ("Slack", "Slack"),
        ("Discord", "Discord"),
        ("Email", "Email"),
    ]
    HACKATHON_EXPERIENCE_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]
    CREATE_TEAM_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    experience = models.TextField()
    hackathon_experience = models.CharField(max_length=5, choices=HACKATHON_EXPERIENCE_CHOICES)
    goal = models.TextField()
    team_status = models.CharField(max_length=20, choices=TEAM_STATUS_CHOICES)
    communication = models.CharField(max_length=20, choices=COMMUNICATION_CHOICES)
    create_team = models.CharField(max_length=10, choices=CREATE_TEAM_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.event.name})"

# -------------------- Sponsorship Model --------------------

class Sponsorship(models.Model):
    TIER_CHOICES = [
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
        ('BRONZE', 'Bronze'),
    ]
    sponsor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sponsorships')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor.user.username} - {self.event.name} - {self.tier}"

# -------------------- Forum Models --------------------

class ForumTopic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='forum_topics')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ForumReply(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='forum_replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.topic.title} by {self.author.user.username}"

# -------------------- Support Ticket Model --------------------

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('RESOLVED', 'Resolved'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"

# -------------------- Messaging Model --------------------

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.user.username} to {self.receiver.user.username}"

# -------------------- Project Model --------------------

class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
