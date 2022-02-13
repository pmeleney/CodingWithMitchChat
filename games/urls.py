from django.urls import path, include

from . import views

app_name = 'games'

urlpatterns = [
    path("", views.ListGames.as_view(), name="all"),
    path("new/", views.CreateGame.as_view(), name="create"),
    path("game/join/<slug:slug>/",views.JoinGame.as_view(),name="join"),
    path("game/<slug:slug>/",views.SingleGame.as_view(),name="game"),
    path("delete/<slug:slug>",views.DeleteGame.as_view(),name="delete"),
    path("newentry/<slug:slug>/",views.NewEntry.as_view(),name="newentry"),
]
