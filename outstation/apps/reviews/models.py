from django.db import models
from outstation.apps.route.models import OutstationRoutePage
#from django.contrib.auth.models import User
from outstation.apps.auth.models import UserProfile
from outstation.apps.framework.models import AdvancedImage
from outstation.apps.core.enums import ReviewStatusChoice


class Review(models.Model):
    title = models.CharField(max_length = 255)
    review_comments = models.TextField(help_text = "Add Review", null = False)
    rating = models.PositiveSmallIntegerField(null = True, blank = True, default = 0)
    publish_date = models.DateTimeField(auto_now_add = True)

    user_profile = models.ForeignKey(UserProfile,
                            related_name = 'user_review',
                            on_delete = models.CASCADE,
                            null = False
                        )

    route = models.ForeignKey(OutstationRoutePage,
                            related_name = 'page_review',
                            on_delete = models.CASCADE,
                            null = False
                        )
    status = models.CharField( max_length = 20, default = ReviewStatusChoice.new.value, null = False)

    def approve(self):
        self.status = ReviewStatusChoice.approved.value
        self.save()

    def reject(self):
        self.status = ReviewStatusChoice.rejected.value
        self.save()

    def __str__(self):
        return self.title


class ReviewImage(models.Model):
    #image = models.ImageField(upload_to = "reviews/images/", null=True)
    image = models.ForeignKey(
            "outstationframework.AdvancedImage",
            null = True,
            blank = False,
            on_delete = models.CASCADE,
            related_name = "+"
        )

    upload_date = models.DateTimeField(auto_now_add = True, null = False)

    review = models.ForeignKey('Review',
                            related_name = 'review_image',
                            null = False,
                            on_delete = models.CASCADE
                        )



class ReviewVideo(models.Model):
    video = models.FileField(upload_to = "reviews/videos/")
    #user = models.ForeignKey(User, related_name='user_review_video', on_delete=models.CASCADE, null=False)
    #route = models.ForeignKey(OutstationRoutePage, related_name='page_review_video', on_delete=models.CASCADE, null=False)
    upload_date = models.DateTimeField(auto_now_add = True, null = False)

    review = models.ForeignKey('Review',
                            related_name = 'review_video',
                            null = False,
                            on_delete = models.CASCADE
                        )
