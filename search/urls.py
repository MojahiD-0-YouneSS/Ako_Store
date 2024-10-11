from django.urls import path
from . import views
app_name = 'search'
urlpatterns = [
    path('results/',views.search_view, name='saerch_by_query'),
    path('add_labels/',views.add_search_labels, name='add_label'),
]
