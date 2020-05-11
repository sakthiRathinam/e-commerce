from django.urls import path
from .views import *
urlpatterns=[
	path('',store,name='store'),
	path('cart/',cart,name='cart'),
	path('checkout/',checkout,name='checkout'),
	path('update_item/',updateItem,name='update'),
	path('process_order/',processOrder,name="process_order"),
	path('login/',loginPage,name="login"),
	path('register/',registerPage,name="register"),
	path('logout/',logoutUser,name='logout'),
	path('customer/',customerCreate,name="customerCreate"),
	path('settings/',profileSettings,name="settings"),
]