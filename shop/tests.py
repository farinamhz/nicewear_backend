from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import override_settings
import tempfile
import shutil
from .models import Comment, Product, Category, SubCategory
from accounts import models
from accounts import views
from model_mommy import mommy

MEDIA_ROOT = tempfile.mkdtemp()


# Create your tests here.
@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ProductCreationTestCase(APITestCase):

    def setUp(self):
        # call_command('loaddata', 'shop/fixtures/categories.json', verbosity=0)
        # call_command('loaddata', 'shop/fixtures/rels.json', verbosity=0)
        self.category1 = Category.objects.create(name="ctest1")
        self.category2 = Category.objects.create(name="ctest2")
        self.crel = SubCategory.objects.create(category=self.category1, sub_category=self.category2)
        # self.user1 = models.User.objects.create(username="seller", password="alaki12345", role=2,
        #                                         email="sellerr@gmail.com")
        self.user1 = mommy.make(models.User, role=2)
        self.user2 = mommy.make(models.User, role=1)
        # self.user1.set_password("alaki12345")
        self.user1.save()
        self.user2.save()
        token1, created1 = Token.objects.get_or_create(user=self.user1)
        token2, created2 = Token.objects.get_or_create(user=self.user2)
        self.token1 = token1.key
        self.token2 = token2.key

        self.f = SimpleUploadedFile(name='test_image.png',
                                    content=b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0d\x49\x44\x41\x54\x78\xda\x63\x64\x60\xf8\x5f\x0f\x00\x02\x87\x01\x80\xeb\x47\xba\x92\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82",
                                    content_type='image/png')

        self.product_context = {
            'picture': self.f,
            'name': "for test",
            'color1': "#test",
            'color2': "#test",
            'color3': "#test",
            'price': 1000,
            'seller': self.user1.pk,
            'category1': self.category1.pk,
            'category2': self.category2.pk,
            'size': "3x",
            'subtitle': "for test subtitile",
        }

    def test_create_product(self):
        self.client.force_authenticate(user=self.user1, token=self.token1)
        response = self.client.post(reverse('create-product'), self.product_context, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class CommentCreationTestCase(APITestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name="ctest1")
        self.category2 = Category.objects.create(name="ctest2")
        self.crel = SubCategory.objects.create(category=self.category1, sub_category=self.category2)
        self.user1 = mommy.make(models.User, role=2)
        self.user2 = mommy.make(models.User, role=1)
        self.user1.save()
        self.user2.save()
        token1, created1 = Token.objects.get_or_create(user=self.user1)
        token2, created2 = Token.objects.get_or_create(user=self.user2)
        self.token1 = token1.key
        self.token2 = token2.key

        self.f = SimpleUploadedFile(name='test_image.png',
                                    content=b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0d\x49\x44\x41\x54\x78\xda\x63\x64\x60\xf8\x5f\x0f\x00\x02\x87\x01\x80\xeb\x47\xba\x92\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82",
                                    content_type='image/png')

        self.product = Product.objects.create(picture=self.f,
                                              name="for test",
                                              color1="#test",
                                              color2="#test",
                                              color3="#test",
                                              price=1000,
                                              seller=self.user1,
                                              category1=self.category1,
                                              category2=self.category2,
                                              size="#test",
                                              subtitle="#test")
        self.comment_context = {
            "user": self.user2.id,
            "product": self.product.id,
            "text": "test"
        }

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user2, token=self.token2)
        response = self.client.post(reverse('create-comment'), self.comment_context, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
