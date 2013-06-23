from wsgiref.simple_server import make_server
from tg import AppConfig, TGController
from tg import expose

FBTOKEN = 'CAACEdEose0cBAAJzx0DKFRN6cQyaVzEN0FTAcqdnf9v5veZAR3ZBHaCxHE8oWrkSFTy2oqh6wNKoaijnZAw77X7G2vhPIKh9zO51R5LaBGbVBMSHy26tJjdU8o8cKbCNRPqOSf6pioQqdrbfYViPVovjxCRKwgZD'

class RootController(TGController):
    @expose('jinja:index.html')
    def index(self, **kw):
        return dict()

    @expose('json:', content_type='application/json')
    def data(self, **kw):
        #print kw['name1']
        query=kw.get('word','')
        return {'query':('').join( sorted(query) )}






config = AppConfig(minimal=True, root_controller=RootController())
config.serve_static = True
config.paths['static_files'] = './'

config.renderers = ['jinja', 'json']
config.default_renderer = 'jinja'

application = config.make_wsgi_app()

print 'Serving on port 8080...'
httpd = make_server('', 8080, application)
httpd.serve_forever()
