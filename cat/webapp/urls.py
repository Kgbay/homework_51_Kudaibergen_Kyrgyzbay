from django.urls import path

from webapp.views.base import index_view, cat_stat_view

urlpatterns = [
    path("", index_view),
    path("cat_stats/", cat_stat_view)
]