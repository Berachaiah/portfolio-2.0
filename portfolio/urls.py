from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('api/chat/', views.ai_chat, name='ai_chat'),
    # Admin dashboard
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/settings/', views.admin_settings, name='admin_settings'),
    path('admin-panel/hero-images/', views.admin_hero_images, name='admin_hero_images'),
    path('admin-panel/hero-images/<int:pk>/delete/', views.admin_hero_image_delete, name='admin_hero_image_delete'),
    path('admin-panel/projects/', views.admin_projects, name='admin_projects'),
    path('admin-panel/projects/new/', views.admin_project_edit, name='admin_project_new'),
    path('admin-panel/projects/<int:pk>/edit/', views.admin_project_edit, name='admin_project_edit'),
    path('admin-panel/projects/<int:pk>/delete/', views.admin_project_delete, name='admin_project_delete'),
    path('admin-panel/certificates/', views.admin_certificates, name='admin_certificates'),
    path('admin-panel/certificates/<int:pk>/delete/', views.admin_cert_delete, name='admin_cert_delete'),
    path('admin-panel/stacks/', views.admin_stacks, name='admin_stacks'),
    path('admin-panel/stacks/<int:pk>/edit/', views.admin_stack_edit, name='admin_stack_edit'),
    path('admin-panel/stacks/<int:pk>/delete/', views.admin_stack_delete, name='admin_stack_delete'),
    path('admin-panel/certificates/<int:pk>/edit/', views.admin_cert_edit, name='admin_cert_edit'),
    path('admin-panel/research/<int:pk>/edit/', views.admin_research_edit, name='admin_research_edit'),
    path('admin-panel/messages/', views.admin_messages_view, name='admin_messages'),
    path('admin-panel/research/', views.admin_research, name='admin_research'),
    path('admin-panel/research/<int:pk>/delete/', views.admin_research_delete, name='admin_research_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
