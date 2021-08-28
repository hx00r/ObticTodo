from django.contrib import admin
from django.urls import path, include
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('submitNew', views.new_to_do_list, name='submitNew'),
    path('get/<str:data_id>', views.get, name='get'),
    path('search/<str:query>', views.search, name='search'),
    # Login and register
    path('login', accountViews.login, name='login'),
    path('register', accountViews.regitser, name='register'),
    path('logout', accountViews.logout, name='logout'),
    path('settings', accountViews.settings, name='settings'),
    path('update', accountViews.update_account, name='update'),
    # handle data here
    path('del_data', views.del_data, name='del_data'),
    path('handle_data', views.handle_data, name='handle_data'),

]
