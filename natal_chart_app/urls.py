
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from chart import views as chart_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chart_view.view_create),
    path('chart/', include('chart.urls'))
]

urlpatterns += staticfiles_urlpatterns()