from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import(LoginRequiredMixin,
                                       PermissionRequiredMixin)
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError, connection
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from games.models import Game, Entry

from django.contrib.auth import get_user_model
from . import forms

import random
from .pp import personal_preferences

from django.core import serializers
import json

User = get_user_model()

# Create your views here.
class NewEntry(LoginRequiredMixin, generic.CreateView):
    model = Entry
    fields = ('entry',)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.game = get_object_or_404(Game,slug=self.kwargs.get("slug"))
        form.instance.place = random.choice(range(9999))
        return super().form_valid(form)

class CreateGame(LoginRequiredMixin, generic.CreateView):
    form_class = forms.GameCreateForm
    model = Game
    success_url = reverse_lazy('games:all')
    template_name = 'games/game_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class SingleGame(LoginRequiredMixin, generic.DetailView):
    model = Game

    def updateUsedNow(self, context):
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE games_entry SET used_now = true WHERE is_used = false AND slug = '{context["game_slug"]}' AND place IN (SELECT place FROM games_entry WHERE is_used = false AND slug = '{context["game_slug"]}' ORDER BY place LIMIT 4);""")

    def updateIsUsed(self, context):
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE games_entry SET is_used = true WHERE used_now = true""")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Update context with game slug
        context['debug_mode'] = settings.DEBUG
        context['game_slug'] = self.kwargs.get("slug")
        context['game_owner'] = self.request.user

        self.updateUsedNow(context)
        context['game_entries'] = serializers.serialize("json", Entry.objects.raw(f"""SELECT *
                                                                                      FROM games_entry
                                                                                      WHERE is_used = false
                                                                                        AND used_now = true
                                                                                        AND slug = '{context['game_slug']}'
                                                                                        ORDER BY place;"""))

        # Update chosen game entries as used
        print(context['game_owner'])
        if context['game_owner'].username.lower() == 'katie':
            print("HERE")
            self.updateIsUsed(context)
        return context

class JoinGame(LoginRequiredMixin, generic.DetailView):
    form_class = forms.GameLoginForm
    model = Game
    template_name = 'games/join_game.html'

class ListGames(LoginRequiredMixin, generic.ListView):
    model = Game

class DeleteGame(LoginRequiredMixin, generic.DeleteView):
    model = Game
    success_url = reverse_lazy('games:all')
