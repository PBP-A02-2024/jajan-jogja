from django.urls import path
from .views import show_main, show_json_tempat, show_json_forum, add_forum_entry_ajax, get_user_by_id, get_current_user_id, delete_forum_entry, edit_forum_entry, add_tempat_kuliner_ajax, edit_tempat_kuliner, delete_tempat_kuliner

app_name = 'alfian'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('json-tempat/', show_json_tempat, name='show_json_tempat'),
    path('json-forum/', show_json_forum, name='show_json_forum'),
    path('edit-forum/<uuid:id>/', edit_forum_entry, name='edit_forum_entry'),
    path('delete-forum/<uuid:id>/', delete_forum_entry, name='delete_forum_entry'),
    path('create-forum-entry-ajax', add_forum_entry_ajax, name='add_forum_entry_ajax'),
    path('get-user/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('get-current-user-id/', get_current_user_id, name='get_current_user_id'),
    path('add-tempat-kuliner-ajax/', add_tempat_kuliner_ajax, name='add_tempat_kuliner_ajax'),
    path('edit-tempat-kuliner/<uuid:id>/', edit_tempat_kuliner, name='edit_tempat_kuliner'),
    path('delete-tempat-kuliner/<uuid:id>/', delete_tempat_kuliner, name='delete_tempat_kuliner'),
]