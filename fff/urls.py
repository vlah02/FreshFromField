# Maksim Mihailovic 2021/0092
# Nikola Kovacevic 2021/0113
# Djordje Loncar 2021/0076
# Marko Vlahovic 2021/0570

from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', home, name="home"),
    path('register/', register, name="register"),
    path('', user_login, name="login"),
    path('chat/<int:chat_id>/', chat, name="chat"),
    path('create_message/<int:chat_id>', create_message, name="create_message"),
    path('chats/', chats, name="chats"),
    path('listings/', listings, name="listings"),
    path('listing/', listing, name="listing"),
    path('logout/', logout_view, name='user_logout'),
    path('newlisting/', new_listing, name='newlisting'),
    path('listings/<str:category>/', listings, name='listings'),
    path('listing/<int:pk>/', listing, name='listing'),
    path('favorites/', favorites, name='favorites'),
    path('change_data/', update_data, name='change_data'),
    path('get_chat/', get_chat, name='get_chat'),
    path('get_chat_admin/', get_chat_admin, name='get_chat'),
    path('edit_listing/<int:pk>/', editListing, name='edit_listing'),
    path('delete_listing/<int:pk>/', deleteListing, name='delete_listing'),
    path('search_listings/', search_listinngs, name='search_listings'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('rate/<int:pk>/', rate, name='rate')
]
urlpatterns += staticfiles_urlpatterns()
