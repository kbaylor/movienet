from django.template import Library

register = Library()

@register.filter
def get_range( value, split=1 ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  split_list = [float(a)/split for a in range(1, (value+1) * split)]
  return  [a for a in split_list if a <= value]