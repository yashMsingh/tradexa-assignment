class AppRouter:
    """
    Routes database operations:
    - users app        → default (db_users.sqlite3)
    - products app     → products_db (db_products.sqlite3)
    - django internals → default
    """

    PRODUCTS_APPS = {'products'}
    USERS_APPS = {'users', 'auth', 'admin', 'contenttypes', 'sessions'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.PRODUCTS_APPS:
            return 'products_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.PRODUCTS_APPS:
            return 'products_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within the same DB group
        db1 = 'products_db' if obj1._meta.app_label in self.PRODUCTS_APPS else 'default'
        db2 = 'products_db' if obj2._meta.app_label in self.PRODUCTS_APPS else 'default'
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.PRODUCTS_APPS:
            return db == 'products_db'
        return db == 'default'
