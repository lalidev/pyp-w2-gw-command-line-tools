import sqlite3
    
class LoginMixin(object):
    """Basic login mixin.

    This mixin will provide the mechanisms to authenticate a user. But it
    doesn't provide authentication by itself.
    It relies in the `authentication` method from other
    Authentication services (like the one shown below).

    You can plug any authentication service that you like, as long
    as it keeps its interface.
    """
    def login(self):
        username = self.request_input_data('username')
        password = self.request_input_data('password')
        self._authenticated_user = self.authenticate(username, password)

        return self._authenticated_user

    @property
    def is_authenticated(self):
        return bool(getattr(self, '_authenticated_user', None) or self.login())

    @property
    def user(self):
        return self._authenticated_user


class SimpleAuthenticationMixin(object):
    AUTHORIZED_USERS = []

    def authenticate(self, username, password):
        for user in self.AUTHORIZED_USERS:
            if user == {'username': username, 'password': password}:
                return user

# Can you think two more authentication services?
# A Json based service and one based on a sqlite3 database?
# Both are builtin modules in Python, should be easy ;)
class DbAuthenticationMixin(object):
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute("create table authorized (username, password)")

    def createDb(self,userTuple):
        for row in userTuple:
            self.cur.execute("insert into authorized values (?,?)",(row[0],row[1] ))
        
    def authenticate(self, username, password):
       # self.con = sqlite3.connect(":memory:")
        sql = "select 1 from authorized where username = ? and password=?"
        c = self.con.cursor()
        c.execute(sql, (username,password))
        if c.fetchone():
            return {'username': username, 'password': password}