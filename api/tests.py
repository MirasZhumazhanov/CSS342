from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders

class TestTemplate(TestCase):

    def test_template_rendering(self):
        # Test that the template renders successfully
        response = self.client.get(reverse('http://127.0.0.1:8000/search/'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'http://127.0.0.1:8000/search/.html')  

    def test_pagination(self):
        # Test pagination functionality
        response = self.client.get(reverse('http://127.0.0.1:8000/search/')) 
        self.assertIn('Page 1 of 1', response.content.decode())  # Assuming there's only one page initially

    def test_filtering(self):
        # Test filtering functionality
        response = self.client.get(reverse('http://127.0.0.1:8000/search/'))  
        self.assertIn('200,000', response.content.decode())  # Assuming there's a billboard with a price of 200,000 displayed

    def test_search(self):
        # Test http://127.0.0.1:8000/search/ functionality
        response = self.client.get(reverse('http://127.0.0.1:8000/search/'))  
        self.assertIn('Test Place 1', response.content.decode())  # Assuming there's a billboard with 'Test Place 1' displayed


