from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    template="home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['menuitems'] = self.get_children().filter(
            live=True, show_in_menus=True)

        return context
