"""
URL configuration for InstaHyreAssignment project.

"""
from django.contrib import admin
from django.urls import path

from FindCallerApp.views import CustomTokenObtainPairView, RegisterView, ReportSpamView, SearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('spam/', ReportSpamView.as_view(), name='spam-report'),
    path('search/', SearchView.as_view(), name='search'),
]
