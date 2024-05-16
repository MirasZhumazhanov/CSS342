from django.test import SimpleTestCase
from django.template import Template, Context

from django.test import SimpleTestCase
from django.template import Template, Context

class TemplateStaticTagTests(SimpleTestCase):
    def test_static_files_are_loaded(self):
        with open('backend\api\templates\api\status.html', 'r') as file:
            template_content = file.read()
        template = Template(template_content)
        rendered = template.render(Context())
        self.assertIn('<link rel="stylesheet" href="/static/css/status.css" />', rendered)

    def test_static_url_is_generated_correctly(self):
        with open('backend\api\templates\api\status.html', 'r') as file:
            template_content = file.read()
        template = Template(template_content)
        rendered = template.render(Context())
        self.assertIn('<img src="/static/images/acc.png" alt="logo" />', rendered)

