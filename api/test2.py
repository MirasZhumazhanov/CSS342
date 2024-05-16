from django.test import TestCase
from django.urls import reverse
from .models import *
from datetime import datetime


class OrderPageTests(TestCase):
    def setUp(self):
        self.billboard = Billboard.objects.create(
            name="Test Billboard",
            address="Test Address",
            category="Test Category",
            city="Test City",
            district="Test District",
            size="Test Size",
            type="Test Type"
        )

    def test_order_page_view(self):
        url = reverse('order_page', kwargs={'pk': self.billboard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/order_page.html')
        self.assertContains(response, 'Test Billboard')
        # Add more assertions as needed


class BookingTests(TestCase):
    def setUp(self):
        self.billboard = Billboard.objects.create(
            name="Test Billboard",
            address="Test Address",
            category="Test Category",
            city="Test City",
            district="Test District",
            size="Test Size",
            type="Test Type"
        )
        self.booking = Booking.objects.create(
            customer_id=1,
            billboard=self.billboard,
            start_date=datetime.now(),
            end_date=datetime.now(),
            total_cost=20000
        )

    def test_get_bookings_view(self):
        url = reverse('get_bookings', kwargs={'pk': self.billboard.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_add_event_view(self):
        url = reverse('add_event')
        data = {
            'user_id': 1,
            'start': '2024-05-06',
            'end': '2024-05-08',
            'billboard_id': self.billboard.pk
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed


class HtmlTemplateTests(TestCase):
    def setUp(self):
        self.billboard = Billboard.objects.create(
            name="Test Billboard",
            address="Test Address",
            category="Test Category",
            city="Test City",
            district="Test District",
            size="Test Size",
            type="Test Type"
        )

    def test_order_page_html(self):
        url = reverse('order_page', kwargs={'pk': self.billboard.pk})
        response = self.client.get(url)
        self.assertContains(response, '<title>Document</title>')
        self.assertContains(response, '<h1>HappyClient</h1>')
        # Add more assertions as needed