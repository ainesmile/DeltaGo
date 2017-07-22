# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.views.services import products


class ProductsViewTest(TestCase):

    def setUp(self):
        client = Client()
        response = client.get('sub_category')
        self.request = response.wsgi_request

    def test_get_categ(self):
        categ = products.get_categ("babycare")
        self.assertEqual(categ, 'B')

    def test_get_sub_categ(self):
        sub_categ = products.get_sub_categ("babycare", "baby-food-from-4-mths")
        self.assertEqual(sub_categ, 'F4')

    def test_get_categs(self):
        categs = products.get_categs("babycare", "baby-food-from-4-mths")
        self.assertEqual(categs, ('B', 'F4'))

    def test_sub(self):
        page = self.request.GET.get("page", 1)
        data = products.sub("babycare", "baby-food-from-4-mths", page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))
        self.assertTrue(data["empty_tips"], "暂无商品，待上架。")
