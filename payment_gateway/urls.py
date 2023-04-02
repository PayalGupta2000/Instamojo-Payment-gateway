from django.urls import path
from .import views
urlpatterns = [
   path("",views.home,name="home"),
   path("order/<product_id>/",views.order,name="order"),
   path("order-success",views.order_success),

]