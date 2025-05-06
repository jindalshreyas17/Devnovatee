from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),  # Account Registration
  
    # Event Registration
    path('participantform/', views.formregisteration, name='participantform'),

    path('event-registration/', views.formregisteration, name='formregisteration'),

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Sponsor Section
    path('sponsor-front/', views.sponsor_front, name='sponsor_front'),
    path('sponsor/create/', views.create_sponsorship, name='create_sponsorship'),
    path('sponsor/create-event/', views.create_event, name='create_event'),
    path('sponsor/profile/', views.update_sponsor_profile, name='update_sponsor_profile'),

    # General Info Pages
    path('about/', views.about, name='about'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('participant_dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('Contact/', views.Contact, name='Contact'),

    # Community Forums
    path('forum/', views.community_forums, name='community_forums'),
    path('forum/create-topic/', views.create_forum_topic, name='create_forum_topic'),
    path('forum/reply/<int:topic_id>/', views.create_forum_reply, name='create_forum_reply'),

    # Networking
    path('sponsor/networking/', views.networking, name='sponsor_networking'),
    path('sponsor/networking/send-message/', views.send_message, name='send_message'),

    # Support
    path('support/', views.support, name='support'),
    path('sponsor/support/', views.support, name='sponsor_support'),
    path('sponsor/support/submit-ticket/', views.submit_support_ticket, name='submit_support_ticket'),
]
