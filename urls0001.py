from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.homepage),
    path('ShowItems/<cid>',views.ShowItems),
    path('ViewDetails/<id>',views.ViewDetails),
    path('Login',views.Login),
    path('SignUp',views.SignUp),
    path('Logout',views.Logout),
    path('AddToCart',views.AddToCart),
    path('ShowAllCartItems',views.ShowAllCartItems),
    path('MakePayment',views.MakePayment),
]
