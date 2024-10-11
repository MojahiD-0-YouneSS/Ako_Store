from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('item/<int:product_id>/', views.post_review, name='post_review'),
    path('item/<int:product_id>/reviews', views.review_list, name='review_list'),
    path('item/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('item/<int:review_id>/reply/', views.reply_to_review, name='reply_to_review'),
    path('user/<int:user_id>/ban/', views.ban_user, name='ban_user'),
    path('reply/<int:reply_id>/', views.hide_reply, name='hide_reply'),
    path('reviews/all/', views.show_reviews, name='all'),
]