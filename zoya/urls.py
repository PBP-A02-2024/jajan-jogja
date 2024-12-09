from django.urls import path
from zoya.views import show_main, show_json_tempat, show_json_forum, add_forum_entry_ajax, get_user_by_id, get_current_user_id, delete_forum_entry, show_json_makanan, edit_forum_entry, create_forum_flutter, edit_forum_flutter, delete_forum_flutter, show_json_user_by_id

app_name = 'zoya'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('json-tempat/', show_json_tempat, name='show_json_tempat'),
    path('json-forum/', show_json_forum, name='show_json_forum'),
    path("json-makanan/", show_json_makanan, name="show_json_makanan"),
    path('edit-forum/<uuid:id>/', edit_forum_entry, name='edit_forum_entry'),
    path('delete-forum/<uuid:id>/', delete_forum_entry, name='delete_forum_entry'),
    path('create-forum-entry-ajax', add_forum_entry_ajax, name='add_forum_entry_ajax'),
    path('get-user/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('json-user/<int:user_id>/', show_json_user_by_id, name='show_json_user_by_id'),
    path('get-current-user-id/', get_current_user_id, name='get_current_user_id'),
    path('create-flutter/', create_forum_flutter, name='create_forum_flutter'),
    path('edit-flutter/', edit_forum_flutter, name='edit_forum_flutter'),
    path('delete-flutter/', delete_forum_flutter, name='delete_forum_flutter'),
]