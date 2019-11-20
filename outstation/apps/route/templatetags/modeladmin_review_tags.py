import datetime

from django.contrib.admin.templatetags.admin_list import ResultList, result_headers
from django.contrib.admin.utils import display_for_field, display_for_value
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from django.db import models
from django.forms.utils import flatatt
from django.template import Library
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from outstation.apps.reviews.models import ReviewImage


register = Library()

def _get_non_gfk_field(opts, name):
    """
    For historical reasons, the admin app relies on GenericForeignKeys as being
    "not found" by get_field(). This could likely be cleaned up.

    Reverse relations should also be excluded as these aren't attributes of the
    model (rather something like `foo_set`).
    """
    field = opts.get_field(name)
    #if (field.is_relation and
            # Generic foreign keys OR reverse relations
    #        ((field.many_to_one and not field.related_model) or field.one_to_many)):
    #    raise FieldDoesNotExist()

    # Avoid coercing <FK>_id fields to FK
    if field.is_relation and not field.many_to_many and hasattr(field, 'attname') and field.attname == name:
        raise FieldIsAForeignKeyColumnName()

    return field


def lookup_field(name, obj, model_admin=None):
    opts = obj._meta
    try:
        f = _get_non_gfk_field(opts, name)
    except (FieldDoesNotExist, FieldIsAForeignKeyColumnName):
        # For non-field values, the value is either a method, property or
        # returned via a callable.
        if callable(name):
            attr = name
            value = attr(obj)
        elif hasattr(model_admin, name) and name != '__str__':
            attr = getattr(model_admin, name)
            value = attr(obj)
        else:
            attr = getattr(obj, name)
            if callable(attr):
                value = attr()
            else:
                value = attr
        f = None
    else:
        attr = None
        if isinstance(f, models.ManyToOneRel):
            value = None
        else:
            value = getattr(obj, name)
    return f, attr, value


def items_for_result(view, result):
    """
    Generates the actual list of data.
    """
    modeladmin = view.model_admin
    for field_name in view.list_display:
        empty_value_display = modeladmin.get_empty_value_display(field_name)
        row_classes = ['field-%s' % field_name]
        try:
            f, attr, value = lookup_field(field_name, result, modeladmin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(
                attr, 'empty_value_display', empty_value_display)
            #print("isinstance(f, models.ManyToOneRel)")
            #print(isinstance(f, models.ManyToOneRel))
            if (f is None or f.auto_created) and not isinstance(f, models.ManyToOneRel) :
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                if boolean or not value:
                    allow_tags = True
                result_repr = display_for_value(
                    value, empty_value_display, boolean)

                # Strip HTML tags in the resulting text, except if the
                # function has an "allow_tags" attribute set to True.
                if allow_tags:
                    result_repr = mark_safe(result_repr)
                if isinstance(value, (datetime.date, datetime.time)):
                    row_classes.append('nowrap')
            else:
                if isinstance(f, models.ManyToOneRel):
                    field_val = getattr(result, f.name)

                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        if(f.name == 'review_image'):
                            image_list = ReviewImage.objects.all().filter(review=result)
                            images=""

                            for img in image_list:
                                img_class= 'review-image-thumbnail'
                                img_src = str(img.image.file.url)
                                #imgstyle = ''
                                img_id = img.image.id
                                modal_class = 'modal-popup'
                                img_modal_class = 'review-image'

                                images = images + "<a class='{}' href='#modalImage-{}'><img src='{}' ></a><div class='{}' id='modalImage-{}'><img  src='{}' class='{}'></div>".format(img_class, img_id, img_src, modal_class, img_id, img_src, img_modal_class)
                            result_repr = images
                        else:
                            result_repr = field_val
                        #print(result_repr)
                else:
                    result_repr = display_for_field(
                        value, f, empty_value_display)

                if isinstance(f, (
                    models.DateField, models.TimeField, models.ForeignKey)
                ):
                    row_classes.append('nowrap')
        if force_text(result_repr) == '':
            result_repr = mark_safe('&nbsp;')
        row_classes.extend(
            modeladmin.get_extra_class_names_for_field_col(result, field_name)
        )
        row_attrs = modeladmin.get_extra_attrs_for_field_col(result, field_name)
        row_attrs['class'] = ' ' . join(row_classes)
        row_attrs_flat = flatatt(row_attrs)
        if(f.name == 'review_image'):
            s = '<td{}>'+result_repr+'</td>'
            yield format_html(s, row_attrs_flat)
        else:
            yield format_html('<td{}>{}</td>', row_attrs_flat, result_repr)


def results(view, object_list):
    for item in object_list:
        yield ResultList(None, items_for_result(view, item))


@register.inclusion_tag("modeladmin/includes/result_list.html",
                        takes_context=True)
def result_list(context):
    """
    Displays the headers and data list together
    """
    view = context['view']
    object_list = context['object_list']
    headers = list(result_headers(view))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1
    context.update({
        'result_headers': headers,
        'num_sorted_fields': num_sorted_fields,
        'results': list(results(view, object_list))})
    return context


@register.simple_tag
def pagination_link_previous(current_page, view):
    if current_page.has_previous():
        previous_page_number0 = current_page.previous_page_number() - 1
        return format_html(
            '<li class="prev"><a href="%s" class="icon icon-arrow-left">%s'
            '</a></li>' %
            (view.get_query_string({view.PAGE_VAR: previous_page_number0}),
                _('Previous'))
        )
    return ''


@register.simple_tag
def pagination_link_next(current_page, view):
    if current_page.has_next():
        next_page_number0 = current_page.next_page_number() - 1
        return format_html(
            '<li class="next"><a href="%s" class="icon icon-arrow-right-after"'
            '>%s</a></li>' %
            (view.get_query_string({view.PAGE_VAR: next_page_number0}),
                _('Next'))
        )
    return ''


@register.inclusion_tag(
    "modeladmin/includes/search_form.html", takes_context=True)
def search_form(context):
    context.update({'search_var': context['view'].SEARCH_VAR})
    return context


@register.simple_tag
def admin_list_filter(view, spec):
    template_name = spec.template
    if template_name == 'admin/filter.html':
        template_name = 'modeladmin/includes/filter.html'
    tpl = get_template(template_name)
    return tpl.render({
        'title': spec.title,
        'choices': list(spec.choices(view)),
        'spec': spec,
    })


@register.inclusion_tag(
    "modeladmin/includes/result_row.html", takes_context=True)
def result_row_display(context, index):
    obj = context['object_list'][index]
    view = context['view']
    row_attrs_dict = view.model_admin.get_extra_attrs_for_row(obj, context)
    row_attrs_dict['data-object-pk'] = obj.pk
    odd_or_even = 'odd' if (index % 2 == 0) else 'even'
    if 'class' in row_attrs_dict:
        row_attrs_dict['class'] += ' %s' % odd_or_even
    else:
        row_attrs_dict['class'] = odd_or_even

    context.update({
        'obj': obj,
        'row_attrs': mark_safe(flatatt(row_attrs_dict)),
        'action_buttons': view.get_buttons_for_obj(obj),
    })
    return context


@register.inclusion_tag(
    "modeladmin/includes/result_row_value.html", takes_context=True)
def result_row_value_display(context, index):
    add_action_buttons = False
    item = context['item']
    closing_tag = mark_safe(item[-5:])
    request = context['request']
    model_admin = context['view'].model_admin
    field_name = model_admin.get_list_display(request)[index]
    if field_name == model_admin.get_list_display_add_buttons(request):
        add_action_buttons = True
        item = mark_safe(item[0:-5])
    context.update({
        'item': item,
        'add_action_buttons': add_action_buttons,
        'closing_tag': closing_tag,
    })
    return context


@register.filter
def get_content_type_for_obj(obj):
    return obj.__class__._meta.verbose_name
