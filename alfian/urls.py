from django.urls import path
from .views import show_main, show_json_tempat, show_json_forum, add_forum_entry_ajax, get_user_by_id, get_current_user_id, delete_forum_entry, edit_forum_entry, add_tempat_kuliner_ajax, edit_tempat_kuliner, delete_tempat_kuliner
from .views import add_makanan_ajax, edit_makanan, delete_makanan, view_tempat_makanan_admin, get_makanan_json, get_restaurant
from .views import create_resto_flutter, edit_resto_flutter, delete_resto_flutter, show_json_variasi
app_name = 'alfian'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('json-tempat/', show_json_tempat, name='show_json_tempat'),
    path('json-forum/', show_json_forum, name='show_json_forum'),
    path('json-variasi/', show_json_variasi, name='show_json_variasi'),
    path('edit-forum/<uuid:id>/', edit_forum_entry, name='edit_forum_entry'),
    path('delete-forum/<uuid:id>/', delete_forum_entry, name='delete_forum_entry'),
    path('create-forum-entry-ajax', add_forum_entry_ajax, name='add_forum_entry_ajax'),
    path('get-user/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('get-current-user-id/', get_current_user_id, name='get_current_user_id'),
    path('add-tempat-kuliner-ajax/', add_tempat_kuliner_ajax, name='add_tempat_kuliner_ajax'),
    path('edit-tempat-kuliner/<uuid:id>/', edit_tempat_kuliner, name='edit_tempat_kuliner'),
    path('delete-tempat-kuliner/<uuid:id>/', delete_tempat_kuliner, name='delete_tempat_kuliner'),
    path('add-makanan-ajax/', add_makanan_ajax, name='add_makanan_ajax'),
    path('edit-makanan/<uuid:id>/', edit_makanan, name='edit_makanan'),
    path('delete-makanan/<uuid:id>/', delete_makanan, name='delete_makanan'),
    path('view-tempat-makanan-admin/<uuid:id>/', view_tempat_makanan_admin, name='view_tempat_makanan_admin'),
    path('get-restaurant/<uuid:tempatKulinerId>/', get_restaurant, name='get_restaurant'),
    path('get-makanan-json/<uuid:tempatKulinerId>/', get_makanan_json, name='get_makanan_json'),
    path('create-resto-flutter/', create_resto_flutter, name='create_resto_flutter'),
    path('edit-resto-flutter/<uuid:id>/', edit_resto_flutter, name='edit_resto_flutter'),
    path('delete-resto-flutter/<uuid:id>/', delete_resto_flutter, name='delete_resto_flutter'),
]