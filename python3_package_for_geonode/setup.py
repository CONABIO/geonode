from setuptools import setup, find_packages

setup(name="geonode_conabio",
      version="0.1",
      description=u"Simplify import of layers into geonode.conabio.gob.mx",
      url="https://github.com/CONABIO/geonode",
      author="CONABIO",
      author_email="",
      license="GPLv3",
      #packages=find_packages(),
      packages=['geonode_conabio'],
      install_requires = [
                          'python-dotenv',
                          'docker',
                          'numpy',
                          'pandas',
                          'geopandas',
                          'rasterio',
                          'fiona'
                          ],
      entry_points = {
          'console_scripts': [
                             'import_raster=geonode_conabio.import_raster:main',
                             'import_small_medium_size_vector=geonode_conabio.import_small_medium_size_vector:main',
                             'import_large_size_vector=geonode_conabio.import_large_size_vector:main',
                             'create_download_link_in_geonode_for_raster=geonode_conabio.create_download_link_in_geonode_for_raster:main',
                             'create_download_link_in_geonode_for_vector=geonode_conabio.create_download_link_in_geonode_for_vector:main'
                             ]
                      }
      )
