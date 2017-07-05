from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.views.babycare import render_data

class BabyCareViewTest(TestCase):

    def setUp(self):
        client = Client()
        response = client.get('babycare')
        self.request = response.wsgi_request

    def test_render_data(self):
        condition =  condition = {"sub_category": "F4"}
        page = self.request.GET.get('page', 1)
        data = render_data(condition, page, 20)
        result_should_be = {
            "products": '<Page 1 of 1>',
            "paginations": '<Page 1 of 1>'
        }
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))
