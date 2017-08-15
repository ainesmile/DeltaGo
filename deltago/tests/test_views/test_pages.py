# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.views.services import page_service
from deltago.models import Commodity

class PagesViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/commodity.json',
    ]

    def setUp(self):
        self.product1 = Commodity.objects.get(pk=1)
        client = Client()
        response = client.get('search')
        request = response.wsgi_request
        self.page = request.GET.get('page', 1)

    def test_search_results(self):
        content_normal = 'Heinz Organic'
        results = page_service.search_results(content_normal, self.page, 20)
        self.assertTrue(isinstance(results["paginations"], Page))
        self.assertTrue(isinstance(results["products"], Page))
        self.assertEqual(results["empty_tips"], "暂无搜索结果，请尝试其他搜索关键词。")

        contents_special = ['', '$']
        for content in contents_special:
            result_special = page_service.search_results(content, self.page, 20)
            self.assertEqual(len(result_special["products"]), 0)
            self.assertEqual(len(result_special["paginations"]), 0)