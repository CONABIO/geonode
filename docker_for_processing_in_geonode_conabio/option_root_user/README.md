Set:

```
JUPYTERLAB_VERSION=2.1.4
REPO_URL=palmoreck/jupyterlab_geopython_for_conabio_cluster_root_user
BUILD_DIR=<path_where_Dockerfile_is>
```

Build:

```
docker build $BUILD_DIR --force-rm -t $REPO_URL:$JUPYTERLAB_VERSION
```

Run:

```
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/datos --name jupyterlab_geopython -p 8888:8888 -d $REPO_URL:$JUPYTERLAB_VERSION
```
