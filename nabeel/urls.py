from django.urls import path
from nabeel.views import create_search_flutter, search_by_keyword, search_page, show_search_history, delete_search_history, show_search_history_by_id, edit_search_history, show_tempat_kuliner_by_category, show_tempat_kuliner_by_keyword, show_variasi

app_name = 'nabeel'

urlpatterns = [
    path('', search_page, name='search_page'),
    path('by-keyword/<str:keyword>', search_by_keyword, name="search_by_keyword"),
    path('show-search-history/', show_search_history, name="show_search_history"),
    path('show-search-history/<str:id>', show_search_history_by_id, name="show_search_history_by_id"),
    path('delete/<str:id>', delete_search_history, name='delete_search_history'),
    path('edit/<str:id>', edit_search_history, name='edit_search_history'),
    path('show-tempat-kuliner-by-category/<str:keyword>-<str:id>', show_tempat_kuliner_by_category, name="show_tempat_kuliner_by_category"),
    path('show-tempat-kuliner-by-keyword/<str:keyword>', show_tempat_kuliner_by_keyword, name="show_tempat_kuliner_by_keyword"),
    path('create-search/', create_search_flutter, name="create_search_flutter"),
    path('show-variasi/', show_variasi, name="show_variasi"),
]