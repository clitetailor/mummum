import ldap3

def authenticate(address, username, password):
    try:
        if len(password) == 0:
            password = "noob"

        server = ldap3.Server("ldap://192.168.4.222")
        conn = ldap3.Connection(server)

        # conn.search()

    except Exception:
        raise "Wrong username or password"
