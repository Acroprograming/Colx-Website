from django.urls import path

from . import views

app_name="colx"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/',views.login,name="login"),
    path('logout/', views.logout, name='logout'),
    path('signup/',views.signup,name="signup"),
    path('sell/',views.sell,name="sell"),
    path('cart/',views.cart,name="cart"),
    path('<int:item_no>/add_to_cart/',views.add_to_cart,name="add_to_cart"),
    path('<int:item_no>/buy/',views.buy,name="buy"),

]