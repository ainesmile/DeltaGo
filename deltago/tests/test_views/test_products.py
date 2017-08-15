# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.paginator import Page

from deltago.models import Commodity, Details
from deltago.views.services import product_service


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
        self.nutrition = u'["385kJ", "320kJ", "0.7g", "0.6g", "1.4g", "1.2g", "17.8g", "14.8g", "16.9g", "14.1g", "3mg", "2mg"]'
        self.e_nutritions = [('Energy', u'385kJ', u'320kJ'), ('Protein', u'0.7g', u'0.6g'), ('Fat - Total', u'1.4g', u'1.2g'), ('Carbohydrate', u'17.8g', u'14.8g'), ('Sugars', u'16.9g', u'14.1g'), ('Sodium', u'3mg', u'2mg')]
        self.e_ingredients = {"note": "1 Organic", "text": "Apples1 (81%), Banana (13.7%), Avocado (5%), Vitamin C"}


    def test_get_categ(self):
        categ = product_service.get_categ("babycare")
        self.assertEqual(categ, 'B')

    def test_get_sub_categ(self):
        sub_categ = product_service.get_sub_categ("babycare", "baby-food-from-4-mths")
        self.assertEqual(sub_categ, 'F4')

    def test_get_categs(self):
        categs = product_service.get_categs("babycare", "baby-food-from-4-mths")
        self.assertEqual(categs, ('B', 'F4'))

    def test_get_sub_navs(self):
        sub_navs = product_service.get_sub_navs("babycare")
        self.assertEqual(sub_navs, self.e_sub_navs)

    def test_sub(self):
        page = self.request.GET.get("page", 1)
        data = product_service.sub("babycare", "baby-food-from-4-mths", page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))
        self.assertTrue(data["empty_tips"], "暂无商品，待上架。")
        self.assertEqual(data["sub_navs"], self.e_sub_navs)
        self.assertEqual(data["categ_name"], "babycare")

    def test_json_loads(self):
        nutrition_list = [u'385kJ', u'320kJ', u'0.7g', u'0.6g', u'1.4g', u'1.2g', u'17.8g', u'14.8g', u'16.9g', u'14.1g', u'3mg', u'2mg']
        data = [
            (self.nutrition, nutrition_list),
            (None, None)
        ]
        for d, r in data:
            self.assertEqual(product_service.json_loads(d), r)
            
    def test_get_nutritions(self):
        result = product_service.get_nutritions(self.nutrition)
        self.assertEqual(result, self.e_nutritions)

    def test_get_details(self):
        data = product_service.get_details(1)
        self.assertEqual(data["product"], self.product1)
        self.assertEqual(data["details"], self.details1)
        self.assertEqual(data["nutritions"], self.e_nutritions)
        self.assertEqual(data["ingredients"], self.e_ingredients)

