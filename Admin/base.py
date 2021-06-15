from flask import request, render_template, redirect, url_for
from user.models import User


class UserChooserForm(object):
    html_template_route = 'admin/user_templates/user_chooser.html'
    route = ''
    title = ''
    model = User
    query = {}

    def action(self, emails: list):
        return NotImplemented('The function "action" if not implemented.')

    def view(self):
        if request.method == 'GET':
            users = [item.get('email') for item in self.model.db().find(*self.query)]
            return render_template(self.html_template_route, users=users, url=f'/admin/{self.route}', title=self.title)
        elif request.method == 'POST':
            emails = request.form.getlist('email')

            self.action(emails)

            return redirect(url_for(f'admin.{self.route.replace("-", "_")}'))

        return '?'
