import os
from analytics.base import Alert, Tip
import json
from flask import request, render_template, url_for, redirect, Blueprint
from flask_login import login_required, login_user, logout_user
from user.models import Admin, User

from flask_restful import Api, Resource

admin = Blueprint('admin', __name__, template_folder='templates')

api = Api(admin)

@admin.route('/admin/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route('/admin/', methods=['GET', 'POST'])
@login_required
def menu():
    return f'<a href="{url_for("admin.reg_a_user")}">register a new user</a>' \
    f'<br><a href="https://admin.melytix.tk/">Tips and Alerts Admin</a>' \
    f'<br><a href="{url_for("admin.logout")}">logout</a>' \
    f'<br><a href="/refresh">refresh metrics</a>'


@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        form = request.form
        login = form.get("login")
        password = form.get("pass")
        if login and password:
            if Admin.verify_password(login, password):
                admin = Admin.get(email=login)
                login_user(admin)
                return redirect(url_for('admin.menu'))
            else:
                return render_template('admin/login/index.html', url='/admin/login', message='wrong credentials')
    elif request.method == 'GET':
        return render_template('admin/login/index.html', url='/admin/login')
    return '?'


@admin.route('/admin/reg-a-user', methods=["GET", "POST"])
@login_required
def reg_a_user():
    if request.method == 'GET':
        return render_template('admin/login/index.html', url='/admin/reg-a-user')
    elif request.method == 'POST':
        form = request.form
        email = form.get("login")
        password = form.get("pass")
        if email and password:
            if not User.get(email=email):
                User.register(email, password)
                return render_template('admin/login/index.html', message='success', url='/admin/reg-a-user')
            else:
                return render_template('admin/login/index.html', message='user with that email already exists', url='/admin/reg-a-user')
    return '?'


class MainManualAnalyzeView(Resource):

    def options(self):
        return {}, 200

    def get(self):
        all_users = User.filter_only(fields={'_id':False, 'email':True, 'Tips':True, 'Alerts':True, 'auth_token':True})

        for user in all_users:
            path = f'users_metrics/{user.get("auth_token")}'
            if os.path.exists(path):
                with open(f'{path}/metrics.json', 'r') as f:
                    metrics = json.loads(f.read())
                    user['metrics'] = metrics

        return {'users': all_users}, 200

    def post(self):
        helper_dict = {
            'Tips': Tip,
            'Alerts': Alert
        }
        user_email = request.json.get('email')
        type_ = request.json.get('type')
        category = request.json.get('category')
        description = request.json.get('description')
        title = request.json.get('title')
        is_human_created = True
        item = helper_dict.get(type_)(
            category=category,
            title=title,
            description=description,
            is_human_created=is_human_created,
            analytics_func=None
        )
        User.append_list(
            {'email': user_email},
            {type_: item.generate()})
        return {'message': 'success'}, 200


api.add_resource(MainManualAnalyzeView, '/admin-api', methods=['OPTIONS', 'POST', 'GET'])