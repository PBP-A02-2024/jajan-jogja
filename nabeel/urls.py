from django.urls import path
from nabeel.views import search_by_keyword, search_page, show_search_history, delete_search_history

app_name = 'nabeel'

urlpatterns = [
    path('', search_page, name='search_page'),
    path('by-keyword/<str:keyword>', search_by_keyword, name="search_by_keyword"),
    path('show-search-history', show_search_history, name="show_search_history"),
    path('delete/<str:id>', delete_search_history, name='delete_search_history'),

]