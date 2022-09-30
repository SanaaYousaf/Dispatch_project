from django.conf.urls.static import static
from django.urls import path

from dispatchproject import settings
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
        path('register/', RegisterView.as_view(), name="register"),
        path('login/', TokenObtainPairView.as_view()),
        path('login/refresh/', TokenRefreshView.as_view()),
        path('verify/', VerifyView.as_view()),
        path('dispatch/', DispatchView.as_view()),
        path('dispatch/<int:pk>/', DispatchDetail.as_view()),
        path('order/', OrderView.as_view(), name='dispatch-order')
        # path('login/', LoginAPIView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

