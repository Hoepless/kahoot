from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from account.views import UserListView, GroupListView
from quiz.views import QuizListView, QuizTakerListView, QuizTakerDetailView, QuizTakerResponseView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/users/', UserListView.as_view()),
    path('api/v1/groups/', GroupListView.as_view()),
    path('api/v1/quizzes/', QuizListView.as_view()),
    path('api/v1/takers/', QuizTakerListView.as_view()),
    path('api/v1/takers/<int:pk>/', QuizTakerDetailView.as_view()),
    path('api/v1/response/', QuizTakerResponseView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)