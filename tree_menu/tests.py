from django.template import Template, Context
from django.test import TestCase
from tree_menu.models import MenuItem
from django.test.utils import CaptureQueriesContext
from django.db import connection

class MenuTagTest(TestCase):
    def setUp(self):
        self.root1 = MenuItem.objects.create(name="Menu1", url="/menu1/", menu_name="main")
        self.root2 = MenuItem.objects.create(name="Menu2", url="/menu2/", menu_name="main")
        self.child1 = MenuItem.objects.create(name="Submenu1", url="/menu2/submenu1/", parent=self.root2, menu_name="main")
        self.child2 = MenuItem.objects.create(name="Submenu2", url="/menu2/submenu2/", parent=self.root2, menu_name="main")
        self.root3 = MenuItem.objects.create(name="Menu3", url="/menu3/", menu_name="main")
        
    def test_draw_menu(self):        
        rendered_menu = self._render_menu("/Menu1/")
        self.assertIn("Menu1", rendered_menu)
        self.assertNotIn("Submenu1", rendered_menu)        

        rendered_menu = self._render_menu("/menu2/")
        self.assertIn("Menu2", rendered_menu)
        self.assertIn("Submenu1", rendered_menu)
        self.assertIn("Submenu2", rendered_menu)
        
        with CaptureQueriesContext(connection) as context:
            self._render_menu("/menu1/")
            self.assertEqual(len(context), 1)
                   
        with CaptureQueriesContext(connection) as context:
            self._render_menu("/menu1/submenu1/")
            self.assertEqual(len(context), 1)

    def _render_menu(self, path):       
        template_str = "{% load menu_tags %}{% draw_menu 'main' %}"
        template = Template(template_str)
        context = Context({"request": self._mock_request(path)})
        return template.render(context)

    def _mock_request(self, path):       
        class MockRequest:
            def __init__(self, path):
                self.path = path
        return MockRequest(path)
