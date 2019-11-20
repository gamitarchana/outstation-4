'''from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse
from django.urls import re_path, include

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        #re_path(r'^review/', include(urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_styleguide_menu_item():
    return MenuItem(
        _('Reviews'),
        reverse('wagalytics_dashboard'),
        classnames='icon icon-fa-bar-chart',
        order=1000
    )'''
