import xmlrpclib
from pprint import pprint

url = 'http://localhost:8069'
db = 'v8dev'
username = 'admin'
password = 'admin'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

search = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True], ['customer', '=', True]]])

searchPag = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True], ['customer', '=', True]]],
    {'offset': 10, 'limit': 5})

#models.execute_kw(db, uid, password, 'res.partner', 'write', [[80], {
 # 'name': "Newer partner"
#}])

#g = models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[80]])

pprint(common.version())
pprint(uid)
pprint(search)
pprint(searchPag)
#pprint(g)