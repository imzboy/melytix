from Admin.views import *
from Admin.base import UserChooserForm

def ind():
    return 'Hi!'

admin.add_url_rule('/ind', 'ind', ind)

for form_class in UserChooserForm.__subclasses__():
    form = form_class()
    rule = f'/{form.route}'
    endpoint = form.route.replace('-', '_')
    view_func = login_required(form.view)

    admin.add_url_rule(rule, endpoint, view_func)
