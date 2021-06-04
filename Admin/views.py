from Admin.utils import build_url
from flask_restful import Api, Resource
from analytics.base import Alert, Tip
from flask import request, render_template, url_for, redirect, Blueprint
from flask_login import login_required, login_user, logout_user
from user.models import Admin, User
import uuid
from Admin.base import UserChooserForm


admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')
api = Api(admin)


'''
simple required endpoints: login, logout and menu
'''

@admin.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))


@admin.route('/login', methods=['GET', 'POST'])
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


@admin.route('/', methods=['GET', 'POST'])
@login_required
def menu():

    base_urls = '<a href="{url_for("admin.reg_a_user")}">register a new user</a>' \
    f'<br><a href="https://admin.melytix.tk/">Tips and Alerts Admin</a>' \
    f'<br><a href="{url_for("admin.logout")}">logout</a>' \
    f'<br><a href="/refresh">refresh metrics</a>' \

    user_chooser_urls = ''

    for form in UserChooserForm.__subclasses__():
        print(form)
        user_chooser_urls += build_url(form.route)

    return base_urls + user_chooser_urls



@admin.route('/reg-a-user', methods=["GET", "POST"])
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


class DeleteUserForm(UserChooserForm):
    title = 'Delete Users'
    user_query = User.db().find({}, {"_id": 0, 'email': 1})
    route = 'delete-users'

    def action(emails: list):
        for email in emails:
            User.delete(email=email)


@admin.route('/individual-emails', methods=["GET", "POST"])
@login_required
def individual_users():

    if request.method == 'GET':
        if emails := User.db().find_one(filter={"type": "email_storage"}):
            result = emails.get('individual_email')
        return render_template('admin/user_templates/user_chooser.html', users=result, url='/admin/individual-emails', title='individual emails')
    elif request.method == 'POST':
        form = request.form.getlist('email')
        emails = User.db().find_one({'type': 'email_storage'}).get('individual_email', [])
        for email in form:
            if emails.count(email):
                emails.remove(email)
        User.db().find_one_and_update(
            {'type': 'email_storage'},
            {'$set': {'individual_email': emails}},
            upsert=True
        )
        return redirect(url_for('admin.individual_users'))


@admin.route('/restore-emails', methods=["GET", "POST"])
@login_required
def restore_emails():
    if request.method == 'GET':
        if emails := User.db().find_one(filter={"type": "email_storage"}):
            result = emails.get('restore_email')
        return render_template('admin/user_templates/user_chooser.html', users=result, url='/admin/restore-emails', title='restore emails')
    elif request.method == 'POST':
        form = request.form.getlist('email')
        emails = User.db().find_one({'type': 'email_storage'}).get('restore_email', [])
        for email in form:
            if emails.count(email):
                emails.remove(email)
        User.db().find_one_and_update(
            {'type': 'email_storage'},
            {'$set': {'restore_email': emails}},
            upsert=True
        )
        return redirect(url_for('admin.restore_emails'))


class ResetAccountForm(UserChooserForm):
    route = 'reset-account'
    title = 'Reset Users(dev)'

    user_query = User.db().find({'connected_systems': {'$exists': True}}, {"_id": 0, 'email': 1})

    def action(emails: list):
        for email in emails:
            User.db().find_one_and_update({'email': email}, {'$unset': {'connected_systems': ''}})

            metrics = User.get(email=email).metrics

            '''write metrics deletion'''


class MainManualAnalyzeView(Resource):

    def options(self):
        return {}, 200

    def get(self):
        all_users = User.filter_only(fields={'_id':True, 'email':True, 'Tips':True, 'Alerts':True, 'auth_token':True})
        for user in all_users:
            metrics = User.get(_id=user.get('_id')).metrics
            sc = metrics.week('search_console')
            ga_f = metrics.week('google_analytics', table_type='filtered')

            user['metrics'] = {
                'search_console': sc,
                'google_analytics': ga_f
            }
            user.pop('_id')

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
            _id=str(uuid.uuid4()),
            category=category,
            title=title,
            description=description,
            is_human_created=is_human_created
        )
        User.append_list(
            {'email': user_email},
            {type_: item.generate()})
        return {'message': 'success'}, 200


class IndividualEmails(Resource):
    def options(self):
        return {}, 200

    def post(self):
        if emails := User.db().find_one(filter={"type": "email_storage"}):
            result = emails.get('individual_email')
            return {'emails': result}, 200
        return {'Message': 'Error, individual emails were not found'}, 400


class RestoreEmails(Resource):
    def options(self):
        return {}, 200

    def post(self):
        if emails := User.db().find_one(filter={"type": "email_storage"}):
            result = emails.get('restore_email')
            return {'emails': result}, 200
        return {'Message': 'Error, emails for restore user`s passwords were not found'}, 400


class RemoveEmail(Resource):
    def options(self):
        return {}, 200

    def post(self):
        email = request.json.get('email')
        category = request.json.get('category')
        emails = User.db().find_one({'type': 'email_storage'}).get(category, [])
        if emails.count(email):
            emails.remove(email)
            User.db().find_one_and_update(
                {'type': 'email_storage'},
                {'$set': {category: emails}},
                upsert=False
            )
            return {'Message': 'success'}, 200
        return {'Message': 'Email not found'}, 400


api.add_resource(MainManualAnalyzeView, '/admin-api', methods=['OPTIONS', 'POST', 'GET'])
api.add_resource(IndividualEmails, '/individual-emails', methods=['OPTIONS', 'POST'])
api.add_resource(RestoreEmails, '/restore-emails', methods=['OPTIONS', 'POST'])
api.add_resource(RemoveEmail, '/remove-email', methods=['OPTIONS', 'POST'])