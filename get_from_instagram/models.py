from django.db import models


class InstagramUser(models.Model):
    '''Instagram user model.'''
    username = models.CharField(max_length=50, null=False)
    full_name = models.CharField(max_length=100)
    instagram_id = models.PositiveIntegerField(null=False)
    followers = models.IntegerField(null=False)
    following = models.IntegerField(null=False)
    is_private = models.BooleanField(default=False)


class InstagramPost(models.Model):
    '''Instagram post model.'''
    post_id = models.PositiveIntegerField(null=False)
    caption = models.CharField(max_length=2200)
    pub_date = models.DateField()
    likes_amount = models.IntegerField()
    coments_amount = models.IntegerField()
    views_amount = models.IntegerField()
    instagram_user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE)


class Media(models.Model):
    '''Instagram media model.'''
    url = models.CharField(max_length=500)
    local_path = models.CharField(max_length=500)
    instagram_post = models.ForeignKey(InstagramPost, on_delete=models.CASCADE)
