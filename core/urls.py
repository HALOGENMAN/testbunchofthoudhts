from django.urls import path
from . import views

urlpatterns =[
     path("",views.BootstrapFilterView,name="bootstrap"),
     path("login",views.login,name="login"),
     path("create",views.create,name="create"),
     path("dashbord",views.dashbord,name="dashbord"),
]