# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.views.services import products

from deltago.models import Commodity

class ProductsViewTest(TestCase):

    def setUp(self):
        client = Client()
        response = client.get('sub_category')
        self.request = response.wsgi_request

    def test_sub(self):
        page = self.request.GET.get("page", 1)
        data = products.sub('B', 'F4', page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))
