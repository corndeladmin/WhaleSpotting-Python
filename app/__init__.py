import os
from flask import Flask, render_template, session
import psycopg2
from flask_migrate import Migrate, upgrade, migrate, stamp
from flask_user import login_required, roles_required, UserManager, user_registered, user_logged_in, user_logged_out
from app.models.user import Member
from app.models.role import Role

from app.models import db

def create_app():
    _create_postgres_database()

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        _update_and_apply_migrations()

    UserManager(app, db, Member)

    # define routes and pages
    @app.route('/')
    def home_page():
        return render_template('index.html')

    @app.route('/members')
    @login_required
    def member_page():
        return render_template('members.html')

    @app.route('/admin')
    @roles_required('Admin')
    def admin_page():
        return render_template('admin.html')

    @user_logged_in.connect_via(app)
    def _on_user_log_in(sender, user):
        session['logged_in'] = True

    @user_logged_out.connect_via(app)
    def _on_user_log_out(sender, user):
        session.pop('logged_in')

    @user_registered.connect_via(app)
    def _after_registration_hook(sender, user, **extra):
        default_role = Role.query.filter_by(name="Member").one()
        user.roles.append(default_role)
        db.session.commit()

        _on_user_log_in(sender, user)

    return app

def _create_postgres_database():
    conn = psycopg2.connect(
        dbname='postgres', # this needs to be defined to establish a server connection
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    cursor = conn.cursor()
    conn.autocommit = True
    try:
        cursor.execute('CREATE DATABASE {}'.format(os.getenv('POSTGRES_DATABASE')))
    except psycopg2.errors.DuplicateDatabase:
        print('Database {} already exists, skipping creation.'.format(os.getenv('POSTGRES_DATABASE')))
    cursor.close()
    conn.close()


def _update_and_apply_migrations():
    # We upgrade() twice - first to apply any migrations that might have been manually added
    # since the app was last run, then to apply migrations created in the migrate() step.
    upgrade()
    migrate()
    upgrade()
