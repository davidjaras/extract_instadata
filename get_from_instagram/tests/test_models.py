from django.test import TestCase
from get_from_instagram.models import InstagramUser, InstagramPost, Media
from datetime import datetime


class InstagramUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        InstagramUser.objects.create(
            username='testing',
            full_name='Test Admetricks',
            instagram_id=123456789,
            followers=1000000,
            following=10
        )

    '''test labels'''

    def test_username_label(self):
        instagram_user = InstagramUser.objects.get(id=1)
        field_label = instagram_user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_full_name_label(self):
        instagram_user = InstagramUser.objects.get(id=1)
        field_label = instagram_user._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'full name')
    
    def test_instagram_id_label(self):
        instagram_user = InstagramUser.objects.get(id=1)
        field_label = instagram_user._meta.get_field('instagram_id').verbose_name
        self.assertEqual(field_label, 'instagram id')
    
    def test_followers_label(self):
        instagram_user = InstagramUser.objects.get(id=1)
        field_label = instagram_user._meta.get_field('followers').verbose_name
        self.assertEqual(field_label, 'followers')
    
    def test_following_label(self):
        instagram_user = InstagramUser.objects.get(id=1)
        field_label = instagram_user._meta.get_field('following').verbose_name
        self.assertEqual(field_label, 'following')
    
    ''' test max length. '''

    def test_username_max_length(self):
        instagram_user = InstagramUser.objects.get(id=1)
        max_length = instagram_user._meta.get_field('username').max_length
        self.assertEqual(max_length, 50)
    
    def test_full_name_max_length(self):
        instagram_user = InstagramUser.objects.get(id=1)
        max_length = instagram_user._meta.get_field('full_name').max_length
        self.assertEqual(max_length, 100)


class InstagramPostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = InstagramUser.objects.create(
            username='testing',
            full_name='Test Admetricks',
            instagram_id=123456789,
            followers=1000000,
            following=10
        )

        InstagramPost.objects.create(
            post_id=123456789,
            caption='Test Admetricks',
            pub_date=datetime.now(),
            likes_amount=1000000,
            coments_amount=10,
            views_amount=0,
            instagram_user=user
        )

    '''test labels'''

    def test_post_id_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('post_id').verbose_name
        self.assertEqual(field_label, 'post id')

    def test_caption_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('caption').verbose_name
        self.assertEqual(field_label, 'caption')
    
    def test_pub_date_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('pub_date').verbose_name
        self.assertEqual(field_label, 'pub date')
    
    def test_likes_amount_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('likes_amount').verbose_name
        self.assertEqual(field_label, 'likes amount')
    
    def test_coments_amount_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('coments_amount').verbose_name
        self.assertEqual(field_label, 'coments amount')
    
    def test_views_amount_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('views_amount').verbose_name
        self.assertEqual(field_label, 'views amount')
    
    def test_instagram_user_label(self):
        instagram_post = InstagramPost.objects.get(id=1)
        field_label = instagram_post._meta.get_field('instagram_user').verbose_name
        self.assertEqual(field_label, 'instagram user')
    
    ''' test max length. '''

    def test_caption_max_length(self):
        instagram_post = InstagramPost.objects.get(id=1)
        max_length = instagram_post._meta.get_field('caption').max_length
        self.assertEqual(max_length, 2200)


class MediaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = InstagramUser.objects.create(
            username='testing',
            full_name='Test Admetricks',
            instagram_id=123456789,
            followers=1000000,
            following=10
        )

        post = InstagramPost.objects.create(
            post_id=123456789,
            caption='Test Admetricks',
            pub_date=datetime.now(),
            likes_amount=1000000,
            coments_amount=10,
            views_amount=0,
            instagram_user=user
        )

        Media.objects.create(
            url='test.sourcemedia.com/test/image/image1.jpg',
            local_path='.media/test/image/image1.jpg',
            instagram_post=post
        )

    '''test labels'''

    def test_url_label(self):
        media = Media.objects.get(id=1)
        field_label = media._meta.get_field('url').verbose_name
        self.assertEqual(field_label, 'url')

    def test_local_path_label(self):
        media = Media.objects.get(id=1)
        field_label = media._meta.get_field('local_path').verbose_name
        self.assertEqual(field_label, 'local path')
    
    def test_instagram_post_label(self):
        media = Media.objects.get(id=1)
        field_label = media._meta.get_field('instagram_post').verbose_name
        self.assertEqual(field_label, 'instagram post')
    
    ''' test max length. '''

    def test_url_max_length(self):
        media = Media.objects.get(id=1)
        max_length = media._meta.get_field('url').max_length
        self.assertEqual(max_length, 500)
    
    def test_local_path_max_length(self):
        media = Media.objects.get(id=1)
        max_length = media._meta.get_field('local_path').max_length
        self.assertEqual(max_length, 500)