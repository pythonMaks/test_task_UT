from django import template
from tree_menu.models import MenuItem
from django.utils.safestring import mark_safe


def get_active_items(current_item, all_items_map):
    active_items = [current_item]
    while current_item.parent_id:
        current_item = all_items_map.get(current_item.parent_id)
        active_items.append(current_item)
    return active_items


def render_menu(item, current_item, active_items, all_items_map):
    html = f'<a href="{item.url}"'
    if item == current_item:
        html += ' class="active"'
    html += f'>{item.name}</a>'
    
    children = [child for child_id, child in all_items_map.items() if child.parent_id == item.id]
    if children and (item == current_item or item in active_items):
        html += '<ul>'
        for child in children:
            html += f'<li>{render_menu(child, current_item, active_items, all_items_map)}</li>'
        html += '</ul>'
    return html


register = template.Library()
@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    all_items = list(MenuItem.objects.filter(menu_name=menu_name).select_related('parent'))

    all_items_map = {item.id: item for item in all_items}
    
    current_url = context['request'].path
    current_item = next((item for item in all_items if item.url == current_url), None)
    
    if not current_item:
        root_items = [item for item in all_items if not item.parent]
        menu_html = ''.join([f'<li>{render_menu(item, None, [], all_items_map)}</li>' for item in root_items])
        return mark_safe(f'<ul>{menu_html}</ul>')

    active_items = get_active_items(current_item, all_items_map)
    menu_items = [item for item in all_items if item.parent is None]
    menu_html = ''.join([f'<li>{render_menu(item, current_item, active_items, all_items_map)}</li>' for item in menu_items])
    return mark_safe(f'<ul>{menu_html}</ul>')


@register.filter
def get_children(item, all_items_map):
    return [child for child_id, child in all_items_map.items() if child.parent_id == item.id]
