from docker import APIClient

def publish_featuretype_via_docker(native_name, user, passwd, epsg_code="EPSG:4326"):
    
    c = APIClient(base_url='unix://var/run/docker.sock')
    
    string = "from geoserver.catalog import Catalog;"
    string2 = "cat = Catalog('http://geonode.conabio.gob.mx' + '/geoserver/rest', \'"
    string3 = "store = cat.get_stores(names=['geonode_data'], workspaces=['geonode']);"
    string4 = "cat.publish_featuretype(native_name, store[0], epsg_code, native_name=native_name)"
    string = "".join([string, string2, 
                      user, "\', ", "\'", passwd, "\');",
                      string3,
                      "native_name = \'", native_name, "\';", 
                      "epsg_code = \'", epsg_code, "\';", 
                      string4])
    cmd = "".join(["python -c ", "\"", string, "\""])
    ex = c.exec_create(container = 'spcgeonode_django_1', 
                       cmd = cmd)
    ex_start = c.exec_start(exec_id=ex)
    return ex_start
    
    

def update_layers_via_docker(layer_name):
    """
    Wrapper for updatelayers command of geonode using docker-py functionality.
    Args:
        layer_name (str): name of layer registered in geoserver
    Returns:
        ex_start (str): result of exec_start method of docker-py
    """
    
    c = APIClient(base_url='unix://var/run/docker.sock')
    cmd = "".join(["python manage.py updatelayers -s geonode_data -w geonode -f ",
                   layer_name, " ",
                   "--settings=geonode.local_settings"])
    ex = c.exec_create(container = 'spcgeonode_django_1', 
                       cmd = cmd)
    ex_start = c.exec_start(exec_id=ex) #if arg stream=True in exec_start method, then returns generator
    return ex_start

def import_layers_via_docker(region, name, title,
                             abstract, keywords, 
                             filename):
    """
    Wrapper for importlayers command of geonode using docker-py functionality.
    Args:
        region (str): name of region registered in geonode
        name (str): name of layer that will be registered in geonode
        title (str): title of layer that will be registered in geonode
        abstract (str): abstract of layer that will be displayed in geonode
        keywords (str): keywords of layer that will be displayed in geonode
        filename (str): path of layer that will be registered in geonode
    Returns:
        ex_start (str): result of exec_start method of docker-py    
    """
    c = APIClient(base_url='unix://var/run/docker.sock')
    cmd = "".join(["python manage.py importlayers -v 3 -i -o ",
                   "-n ", name, " ",
                   "-t ", title, " ",
                   "-a ", abstract, " ",
                   "-k ", keywords, " ",
                   "-r ", region, " ",
                   filename, " ",
                   "--settings=geonode.local_settings"])
    ex = c.exec_create(container = 'spcgeonode_django_1', 
                       cmd = cmd)
    ex_start = c.exec_start(exec_id=ex) #if arg stream=True in exec_start method, then returns generator
    
    return ex_start