"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper


def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect(':title', controller='root', action='index')
    map.connect('home', '/', controller='root', action="index")
    map.connect(None, '/xmlrpc', controller='MasterXMLRPC')
    map.connect(None, '/xmlrpc/', controller='MasterXMLRPC')
    map.connect(None, '/{controller}')
    map.connect(None, '/{controller}/{action}')
    map.connect(None, '/{controller}/{action}/{id}')
    map.connect(None, '/{controller}/{action}/{id}/filter/{filter}')
    map.connect('list', '/{controller}/list', action="list")
    map.connect(None, '/{controller}/{action}/{id}/period/{period}')
    map.connect(None, '/{controller}/{action}/{id}/start_date/{start_date}')
    map.connect(None,
                '/{controller}/{action}/{id}/start_date/{start_date}/filter/{filter}')
    map.connect(
        None, '/{controller}/{action}/{id}/start_date/{start_date}/end_date/{end_date}')
    map.connect(
        None, '/{controller}/{action}/{id}/period/{period}/start_date/{start_date}')
    map.connect(
        None, '/{controller}/{action}/{id}/period/{period}/start_date/{start_date}/end_date/{end_date}')
    map.connect(None, '/{controller}/{action}/what/{what}/how_many/{how_many}')
    map.connect(
        None, '/{controller}/{action}/what/{what}/how_many/{how_many}/period/{period}')

    map.redirect('/*(url)/', '/{url}', _redirect_code='301 Moved Permanently')

    return map
