from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin




urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('cars/', views.car_list, name='car_list'),
    path('register/', views.register_view, name='register'),
    path('admin/', admin.site.urls),
    path('cars/category/<str:category_name>/', views.category_view, name='category_view'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('logout/', views.logout_view, name='logout'),

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)