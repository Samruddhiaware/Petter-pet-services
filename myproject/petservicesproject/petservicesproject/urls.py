"""
URL configuration for petservicesproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from mypetapp.views import Serviceview, SPRequestList, Servicedetail, SPServiceList, SPcreateservice, SPdetailservice, SPupdateservice, SPdeleteservice
from django.conf import settings
from django.conf.urls.static import static
from mypetapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('serviceview/', Serviceview.as_view(), name='serviceview'),
    path('filter/<str:location>', views.filterservicebylocation, name='filterbylocation'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('servicedetail/<int:pk>/', Servicedetail.as_view(), name='servicedetail'),
    path('addtocart/', views.addtocart, name='addtocart'),   
    path('viewcart/', views.viewcart, name='viewcart'),
    path('removefromcart/', views.removefromcart, name='removefromcart'),
    # path('booking/', views.booking, name='booking'),
    path('spbookingdecision/', views.spbookingdecision, name='spbookingdecision'),
    path('accept/', views.accept, name='accept'),
    path('reject/', views.reject, name='reject'),
    # path('checkbkstatus/', views.checkbkstatus, name='checkbkstatus'),
    path('summary/', views.summary, name='summary'),
    path('payment/', views.payment, name='payment'),
    path('paymentsuccess', views.paymentsuccess, name='paymentsuccess'),
    path('spservicelist/', SPServiceList.as_view(), name="spservicelist"),
    path('sprequestlist/', SPRequestList.as_view(), name="requestview"),
    path('spcreateservice/', SPcreateservice.as_view(),name="spcreateservice"),
    path('spupdateservice/<int:pk>/', SPupdateservice.as_view(),name="spupdateservice"),
    path('spdetailservice/<int:pk>/', SPdetailservice.as_view(),name='spdetailservice'),
    path('spdeleteservice/<int:pk>/', SPdeleteservice.as_view(),name='spdeleteservice'),
    path('logout', views.logout, name='logout'),  
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
