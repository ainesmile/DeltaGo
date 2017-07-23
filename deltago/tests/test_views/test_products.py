# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.views.services import products

from deltago.models import Commodity, Details


class ProductsViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/commodity.json',
        'deltago/fixtures/details.json',
    ]

    def setUp(self):
        client = Client()
        response = client.get('sub_category')
        self.request = response.wsgi_request

        self.e_sub_navs = [
            {
                "name": "baby-food-from-4-mths",
                "text": "辅食・4月+"
            },
            {
                "name": "baby-food-from-6-mths",
                "text": "辅食・6月+"
            },
            {
                "name": "baby-food-from-9-mths",
                "text": "辅食・9月+"
            },
            {
                "name": "baby-food-from-12-mths",
                "text": "辅食・12月+"
            },
            {
                "name": "other-baby-foods",
                "text": "辅食・其他"
            },
            {
                "name": "medicinal-needs",
                "text": "医疗"
            },
            {
                "name": "nappies-liners",
                "text": "纸尿布"
            }
        ]

        self.product1 = Commodity.objects.get(pk=1)
        self.details1 = Details.objects.get(pk=1)

    def test_get_categ(self):
        categ = products.get_categ("babycare")
        self.assertEqual(categ, 'B')

    def test_get_sub_categ(self):
        sub_categ = products.get_sub_categ("babycare", "baby-food-from-4-mths")
        self.assertEqual(sub_categ, 'F4')

    def test_get_categs(self):
        categs = products.get_categs("babycare", "baby-food-from-4-mths")
        self.assertEqual(categs, ('B', 'F4'))

    def test_get_sub_navs(self):
        sub_navs = products.get_sub_navs("babycare")
        self.assertEqual(sub_navs, self.e_sub_navs)

    def test_sub(self):
        page = self.request.GET.get("page", 1)
        data = products.sub("babycare", "baby-food-from-4-mths", page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))
        self.assertTrue(data["empty_tips"], "暂无商品，待上架。")
        self.assertEqual(data["sub_navs"], self.e_sub_navs)
        self.assertEqual(data["categ_name"], "babycare")

    def test_get_details(self):
        data = products.get_details(1)
        self.assertEqual(data["product"], self.product1)
        self.assertEqual(data["details"], self.details1)

    

