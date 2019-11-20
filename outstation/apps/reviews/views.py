from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Review, ReviewImage, ReviewVideo
from outstation.apps.route.models import OutstationRoutePage
from outstation.apps.auth.models import UserProfile
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from outstation.apps.framework.models import AdvancedImage
from django.conf import settings
from django.core.mail import send_mail
from wagtail.contrib.modeladmin.views import InstanceSpecificView, IndexView, EditView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.functional import cached_property

from antispam import akismet

def review_list(request, route_id):
    if (route_id and route_id.strip and Review.objects.all().filter(route_id=route_id).exists()):
        reviews = Review.objects.all().filter(route_id=route_id).order_by('-publish_date')
        return render(request, 'reviews/review_list.html', {'reviews': reviews})
    return render(request, 'reviews/review_list.html',{'reviews':''})

def review(request):

    if request.method == 'POST':
        reviewTitle = request.POST.get('reviewTitle')
        reviewComments = request.POST.get('reviewComments')
        reviewRating = request.POST.get('reviewRating')
        user_profile = get_object_or_404(UserProfile, user_id=request.user.id)
        route_id = request.POST.get('route_id')
        data = {}

        if akismet.check(
            request=akismet.Request.from_django_request(request),
            comment=akismet.Comment(
                content=reviewTitle,
                type='comment',
                author=akismet.Author(
                    name=user_profile.user.username,
                    email=user_profile.user.email
                )
            )
        ):
            print('Title Spam detected')
            data['is_title_spam'] = True;
        if akismet.check(
            request=akismet.Request.from_django_request(request),
            comment=akismet.Comment(
                content=reviewComments,
                type='comment',
                author=akismet.Author(
                    name=user_profile.user.username,
                    email=user_profile.user.email
                )
            )
        ):
            data['is_comment_spam'] = True;

        if data:
            return JsonResponse(data)
        if not data:
            route = get_object_or_404(OutstationRoutePage, id=request.POST.get('route_id'))
            user_review = Review.objects.create(
                title = reviewTitle,
                review_comments = reviewComments,
                rating = reviewRating,
                user_profile = user_profile,
                route = route
            )
            for key in request.FILES:
                if 'images' in key:
                    image_file = request.FILES[key]
                    image_name = request.FILES[key].name
                    image = AdvancedImage.objects.create(
                        title = image_name,
                        file = image_file,
                        upload_folder='reviews/images/'
                    )

                    ReviewImage.objects.create(image=image, review=user_review)
                if 'videos' in key:
                    video_file = request.FILES[key]
                    ReviewVideo.objects.create(video=video_file, review=user_review)
            count=route.page_review.count()
            reviews = Review.objects.all().filter(route_id=route_id).order_by('-publish_date')
            #return render(request, 'reviews/review_list.html', {'reviews': reviews, 'count':count})
            from django.core.mail import send_mail

            send_mail(
                'Test notification',
                'Review content.',
                settings.EMAIL_HOST_USER,
                ['archanangamit@gmail.com'],
                fail_silently=False,
            )
            return JsonResponse({'total_reviews':count})
            #return render(request, 'reviews/review_list.html', reviews)

    return render(request, 'reviews/review.html')

class ApprovedListView(IndexView):
    def get_base_queryset(self, request=None):
        print("ApprovedView - get_base_queryset")
        return self.model_admin.get_approved_queryset(request or self.request)

    #def get_template_names(self):
    #    return self.model_admin.get_index_template()

    def get_buttons_for_obj(self, obj):
        return self.button_helper.get_buttons_for_approved_list_obj(
            obj, classnames_add=['button-small', 'button-secondary'])

class ReviewInstanceSpecificView():
    @cached_property
    def approve_url(self):
        return self.url_helper.get_action_url('approve', self.pk_quoted)

    @cached_property
    def reject_url(self):
        return self.url_helper.get_action_url('reject', self.pk_quoted)

class ReviewEditView(EditView, ReviewInstanceSpecificView):
    def get_review_images_objectList(self):
        imageList = ReviewImage.objects.all().filter(review_id=self.instance_pk)
        for img in imageList:
            print("------------")
            print(img.image.file.url)
        return imageList

    def get_context_data(self, **kwargs):
        imageList = self.get_review_images_objectList()
        print(self.instance_pk)
        context = {'imageList': imageList}
        context.update(kwargs)
        return super().get_context_data(**context)



class ApproveView(InstanceSpecificView, ReviewInstanceSpecificView):
    page_title = _('Approve')

    '''def check_action_permitted(self, user):
        return self.permission_helper.user_can_delete_obj(user, self.instance)'''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_action_permitted(request.user):
            raise PermissionDenied
        '''if self.is_pagemodel:
            return redirect(
                self.url_helper.get_action_url('delete', self.pk_quoted)
            )'''
        return super().dispatch(request, *args, **kwargs)

    '''def get_meta_title(self):
        return _('Confirm deletion of %s') % self.verbose_name'''

    def confirmation_message(self):
        return _(
            "Are you sure you want to approve this %s? "
        ) % self.verbose_name

    def approve_instance(self):
        self.instance.approve()

    def post(self, request, *args, **kwargs):
        try:
            msg = _("{model} '{instance}' deleted.").format(
                model=self.verbose_name, instance=self.instance)

            #print("--self.index_url--")
            #print(self.index_url)
            self.approve_instance()
            #print("--self.index_url-----")
            #print(self.index_url)
            #messages.success(request, msg)
            #print("self.index_url")
            #print(self.index_url)
            return redirect(self.index_url)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
            '''models.ProtectedError:
            linked_objects = []
            fields = self.model._meta.fields_map.values()
            fields = (obj for obj in fields if not isinstance(
                obj.field, ManyToManyField))
            for rel in fields:
                if rel.on_delete == models.PROTECT:
                    qs = getattr(self.instance, rel.get_accessor_name())
                    for obj in qs.all():
                        linked_objects.append(obj)
            context = self.get_context_data(
                protected_error=True,
                linked_objects=linked_objects
            )
            return self.render_to_response(context)'''


    def get_template_names(self):
        return self.model_admin.get_approve_template()




class RejectView(InstanceSpecificView, ReviewInstanceSpecificView):
    page_title = _('Reject')

    '''def check_action_permitted(self, user):
        return self.permission_helper.user_can_delete_obj(user, self.instance)'''

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_action_permitted(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    '''def get_meta_title(self):
        return _('Confirm deletion of %s') % self.verbose_name'''

    def confirmation_message(self):
        return _(
            "Are you sure you want to reject this %s? "
        ) % self.verbose_name

    def reject_instance(self):
        self.instance.reject()

    def post(self, request, *args, **kwargs):
        try:
            msg = _("{model} '{instance}' deleted.").format(
                model=self.verbose_name, instance=self.instance)

            self.reject_instance()
            #messages.success(request, msg)
            return redirect(self.index_url)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def get_template_names(self):
        return self.model_admin.get_reject_template()
