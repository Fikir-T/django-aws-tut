from django.urls import path
from .views import shop,detail,search


app_name = 'item'
urlpatterns = [
    path('shop/', shop , name='shop'),
    path('shop/<int:pk>/', detail, name='detail'),
    path('search/', search, name='search'),
    # path('add_review/', add_review,name='review_view')
]