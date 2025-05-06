# core/admin.py
from django.contrib import admin
from .models import Profile, Team, Event, Sponsorship, Project, ForumTopic, ForumReply, SupportTicket, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company_name', 'contact_info')
    search_fields = ('user__username', 'role', 'company_name', 'contact_info')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'is_online', 'is_offline', 'is_hybrid', 'status']


@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'event', 'amount', 'tier', 'created_at')
    search_fields = ('sponsor__user__username', 'tier')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'created_at')
    search_fields = ('title', 'team__name')

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__user__username')

@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at')
    search_fields = ('topic__title', 'author__user__username')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    search_fields = ('subject', 'user__user__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sent_at')
    search_fields = ('sender__user__username', 'receiver__user__username')