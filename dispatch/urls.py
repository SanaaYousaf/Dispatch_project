from django.conf.urls.static import static
from django.urls import path

from dispatchproject import settings
from .views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
        path('register/', RegisterView.as_view(), name="register"),
        path('login/', TokenObtainPairView.as_view(), name="login"),
        path('login/refresh/', TokenRefreshView.as_view()),
        path('verify/', VerifyView.as_view(), name="verify"),
        path('dispatch/', DispatchView.as_view(), name="dispatch"),
        path('dispatch/<int:pk>/', DispatchDetail.as_view(), name="dispatch_detail"),
        path('order/', OrderView.as_view(), name='dispatch-order')
        # path('login/', LoginAPIView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

