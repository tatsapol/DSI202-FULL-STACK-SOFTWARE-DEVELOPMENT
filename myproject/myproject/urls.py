"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include # new
from myapp import views # new
from myapp.views import *
#from django.contrib.auth.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/',views.profile, name='profile'),
    path('', ItemListView.as_view(),name='home'),
    path('add', views.add_to_cart, name='add'),
    path('accounts/', include('allauth.urls')), # new
    path('about/',views.About, name='about'),
    path('checkout/',views.Pay, name='pay'),
    # path('cart/', views.cart_list.as_view(),name='cart'),
    path('cart/', views.cart_list, name='cart'),
    path('detail/<int:id>', views.product_detail, name='detail' ),
    path('logout/', views.Logout_view, name='logout'),
    path('qr_mobile/<mobile>/<amount>/qr.png', views.get_qr, name='qr'),
    path('qr_nid/<nid>/<amount>/', views.get_qr, name='qr'),
    path('record/', RecordListView.as_view(),name='record'),
    ]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
