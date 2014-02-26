import hashlib
import sys

from CodernityDB.database import Database

from papaye.indexes import INDEXES
from papaye.scripts.common import get_settings


DEFAULT_PERMISSIONS = {
    'admin': (
        'admin',
        'install',
        'publish',
    ),
    'publisher': (
        'install',
        'publish',
    ),
    'installer': (
        'download',
    ),
}


def create_db(settings):
    database_path = settings['codernity.url'][7:]
    db = Database(database_path)
    if not db.exists():
        print("Create Database at {}".format(db.path))
        db.create()
        for name, index_class in INDEXES:
            index = index_class(db.path, name)
            db.add_index(index)
        for key, value in DEFAULT_PERMISSIONS.items():
            group = {
                'name': key,
                'type': 'group',
                'permissions': value,
            }
            db.insert(group)
        create_admin_user(db)
    else:
        print("Database already exists at {}".format(db.path))
        db.open(db)
    return db


def create_admin_user(db):
    username = raw_input('Username for administrator (default="admin"): ')
    username = 'admin' if not username or username == '' else username
    password = raw_input('Password: ')
    admin = {
        'username': username,
        'password': hashlib.sha256(password).digest(),
        'group': 'admin',
        'type': 'user',
    }
    db.insert(admin)


def main(*argv, **kwargs):
    settings = get_settings(sys.argv[1])
    create_db(settings)
    print("Initialization complete!")