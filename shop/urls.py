from django.contrib import admin
from django.urls import path
from accounts.views import login_user, logout_user, signup
from store.views import add_to_cart, cart, confirm_cart, delete_cart, delete_product, index, modify_product, product_detail


urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('cart/', cart, name='cart'),
    path('cart/delete', delete_cart, name='delete-cart'),  
    #path('cart/confirm', confirm_cart, name='confirm-cart'),  
    path('product/<str:id>/', product_detail, name="product"),
    path('product/<str:id>/delete', delete_product, name="delete-product"),
    path('product/<str:id>/add-to-cart', add_to_cart, name="add-to-cart"),
    path('product/<str:id>/modify/', modify_product, name="modify-product")
]
