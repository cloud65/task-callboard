from django import template
register = template.Library()

@register.simple_tag
def setvar(val=None):
  return val
  
  
@register.filter
def parse_image(html=None):
    if html is None:
        return None
    b = html.find('<img')
    if b==-1:
        return None
    b =  html.find('src', b)    
    b =  html.find('"', b)+1
    e =  html.find('"', b)
    return html[b:e]