#from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,

)
from .models import Review
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtail.contrib.modeladmin.helpers import ButtonHelper, AdminURLHelper
from django.contrib.admin.utils import quote
from django.utils.translation import ugettext as _
from .views import ApproveView, RejectView, ApprovedListView, ReviewEditView
from django.conf.urls import url
from outstation.apps.core.enums import ReviewStatusChoice

# Register your models here.

class ReviewButtonHelper(ButtonHelper):
    approve_button_classnames = []
    reject_button_classnames = []
    def approve_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.approve_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        print("---------------")
        print(self.url_helper.get_action_url('approve', quote(pk)))
        return {
            'url': self.url_helper.get_action_url('approve', quote(pk)),
            'label': _('Approve %s') % self.verbose_name,
            'classname': cn,
            'title': _('Approve this %s') % self.verbose_name,
        }

    def reject_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.reject_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.get_action_url('reject', quote(pk)),
            'label': _('Reject %s') % self.verbose_name,
            'classname': cn,
            'title': _('Reject this %s') % self.verbose_name,
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        if exclude is None:
            exclude = []
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        ph = self.permission_helper
        usr = self.request.user
        pk = getattr(obj, self.opts.pk.attname)
        btns = []
        if('inspect' not in exclude and ph.user_can_inspect_obj(usr, obj)):
            btns.append(
                self.inspect_button(pk, classnames_add, classnames_exclude)
            )
        if('edit' not in exclude and ph.user_can_edit_obj(usr, obj)):
            btns.append(
                self.edit_button(pk, classnames_add, classnames_exclude)
            )
        if('delete' not in exclude and ph.user_can_delete_obj(usr, obj)):
            btns.append(
                self.delete_button(pk, classnames_add, classnames_exclude)
            )
        if('approve' not in exclude and ph.user_can_edit_obj(usr, obj)):
            btns.append(
                self.approve_button(pk, classnames_add, classnames_exclude)
            )
        if('reject' not in exclude and ph.user_can_edit_obj(usr, obj)):
            btns.append(
                self.reject_button(pk, classnames_add, classnames_exclude)
            )
        return btns

    def get_buttons_for_approved_list_obj(self, obj, exclude=None, classnames_add=None,
                    classnames_exclude=None):
        if exclude is None:
            exclude = []
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        ph = self.permission_helper
        usr = self.request.user
        pk = getattr(obj, self.opts.pk.attname)
        btns = []
        if('inspect' not in exclude and ph.user_can_inspect_obj(usr, obj)):
            btns.append(
                self.inspect_button(pk, classnames_add, classnames_exclude)
            )
        if('edit' not in exclude and ph.user_can_edit_obj(usr, obj)):
            btns.append(
                self.edit_button(pk, classnames_add, classnames_exclude)
            )
        if('delete' not in exclude and ph.user_can_delete_obj(usr, obj)):
            btns.append(
                self.delete_button(pk, classnames_add, classnames_exclude)
            )
        if('reject' not in exclude and ph.user_can_edit_obj(usr, obj)):
            btns.append(
                self.reject_button(pk, classnames_add, classnames_exclude)
            )
        return btns


class ReviewURLHelper(AdminURLHelper):
    def get_action_url_pattern(self, action):
        if action in ('create', 'choose_parent', 'index', 'approved_list'):
            return self._get_action_url_pattern(action)
        return self._get_object_specific_action_url_pattern(action)

class SubscriberReview(ModelAdmin):
    model = Review
    menu_label = "Reviews"
    menu_icon = "placeholder"
    menu_order = 2
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("route", "title", "review_comments", "rating", "review_image", "publish_date", "status")
    #list_display = ("route", "title", "review_comments", "rating", "publish_date", "status")
    #fields = (readonly_fields"title", "review_comments", "rating", "publish_date")
    #search_fields = ("title")
    button_helper_class = ReviewButtonHelper
    url_helper_class = ReviewURLHelper
    approve_view_class = ApproveView
    approve_template_name = ''
    reject_view_class = RejectView
    reject_template_name = ''
    approved_list_view_class = ApprovedListView
    approved_list_template_name = ''
    edit_view_class = ReviewEditView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls = urls + (
                url(self.url_helper.get_action_url_pattern('approved_list'),
                    self.approved_list_view,
                    name=self.url_helper.get_action_url_name('approved_list')),
                url(self.url_helper.get_action_url_pattern('approve'),
                    self.approve_view,
                    name=self.url_helper.get_action_url_name('approve')),
                url(self.url_helper.get_action_url_pattern('reject'),
                    self.reject_view,
                    name=self.url_helper.get_action_url_name('reject')),

                #url(r'^admin/outstationreview/review/approved', self.approved_list_view),
        )
        #print(self.url_helper.get_action_url_name('approved_list'))
        #print(self.url_helper.get_action_url_pattern('approved_list'))
        #print(self.url_helper.get_action_url_pattern('index'))
        #print(self.url_helper.get_action_url_name('create'))
        return urls
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print("get_queryset")
        ls = qs.filter(status = ReviewStatusChoice.new.value)
        #for item in ls:
        #    print(item.title)
        return qs.filter(status = ReviewStatusChoice.new.value)

    def get_approved_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(status = ReviewStatusChoice.approved.value)

    def approve_view(self, request, instance_pk):
        """
        Instantiates a class-based view to provide 'approve confirmation'
        functionality for the assigned model.
        """
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.approve_view_class
        return view_class.as_view(**kwargs)(request)

    def get_approve_template(self):
        """
        Returns a template to be used when rendering 'approve_view'.
        """
        return self.approve_template_name or self.get_templates('approve')

    def reject_view(self, request, instance_pk):
        """
        Instantiates a class-based view to provide 'reject confirmation'
        functionality for the assigned model.
        """
        kwargs = {'model_admin': self, 'instance_pk': instance_pk}
        view_class = self.reject_view_class
        return view_class.as_view(**kwargs)(request)

    def get_reject_template(self):
        """
        Returns a template to be used when rendering 'reject_view'.
        """
        return self.reject_template_name or self.get_templates('reject')

    def approved_list_view(self, request):
        """
        Instantiates a class-based view to provide 'approve confirmation'
        functionality for the assigned model.
        """
        print("approved_list_view")
        kwargs = {'model_admin': self}
        view_class = self.approved_list_view_class
        return view_class.as_view(**kwargs)(request)

    def get_approved_list_template(self):
        """
        Returns a template to be used when rendering 'approve_view'.
        """
        return self.approved_list_template_name or self.get_templates('index')



modeladmin_register(SubscriberReview)
