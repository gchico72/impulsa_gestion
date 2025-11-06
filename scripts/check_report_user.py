import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
username = 'report_viewer'
cur.execute("select id,username,email,is_active,is_staff,is_superuser from auth_user where username=?", (username,))
row = cur.fetchone()
if not row:
    print('NOT_FOUND')
else:
    print('FOUND', row)
cur.execute("select p.codename from auth_permission p join django_content_type ct on p.content_type_id=ct.id where p.id in (select permission_id from auth_user_user_permissions up where up.user_id=(select id from auth_user where username=?))", (username,))
perms = cur.fetchall()
print('user_perms=', [p[0] for p in perms])
con.close()
