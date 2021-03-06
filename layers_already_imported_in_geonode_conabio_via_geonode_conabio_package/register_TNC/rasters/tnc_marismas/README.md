
# Registration in geonode of TNC data (rasters)

## Note: this README is using implementation of geonode_conabio package before (including) [commit](https://github.com/CONABIO/geonode/tree/efebe371342273111e1533c75ee4f32242b3bfc2)

Base dir:

```
/LUSTRE/MADMEX/tnc_data_steffen_thilo/tnc_marismas/
```

Shell script:

`register_TNC_rasters.sh`

```
#!/bin/bash

#base dir in $1
#filename in $2

level=$(echo $2|sed -n 's/.*_2019_\(.*\)_final.*/\1/;p')
if [ $level == "nivel1" ]; then
  classes="8"
else
  classes="13"
fi
year=2018_2019
region="Marismas Nacionales, Mexico, North America, Latin America"
name="MAD-Mex_TNC_marismas_nacionales_landsat8_rapideye_lc_$(echo $year)_$(echo $classes)_classes"
title="Cobertura de suelo TNC marismas nacionales 2018, 2019 $(echo $classes) clases"
kw="MAD-Mex, Landsat8, RapidEye, GeoTIFF"
abstract="El mapa de cobertura de suelo 2018, 2019 en la region de marismas nacionales, es un producto geografico digital generado a partir de imagenes RapidEye (2019) complementadas con imagenes Landsat8 (2018). Encierra informacion en base a una clasificacion realizada por MAD-Mex de 8 y 13 grupos de coberturas de vegetacion y usos. Es el resultado de 2 procesos basicos; por un lado una clasificacion automatizada y posteriormente una revision, analisis, correccion y ajuste de esa operacion. La ordenacion o agrupamiento en 8 y 13 clases se basa en la clasificacion de los tipos de vegetacion y usos de suelo del pais que establece el INEGI. Se representan conjuntos de elementos que sobre el terreno son equivalentes o mayores a 0.5 Has. Se realizo una estimacion de exactitud del mapa de cobertura de suelo usando un conjunto de 1043 objetos aleatorios. Se evaluaron las 8 clases MAD-Mex. La exactitud global calcula 78.72%. Las precisiones de las clases (PPV, Precision or positive predictive value) se calculan 93.92% (Manglar y Peten), 83.72% (Tierras Agricolas), 96.3% (Urbano y Construido), 85.31% (Agua), 58.33% (Selva Baja Caducifolia Subcaducifolia y Matorral Subtropical con mayores confusiones con Tierras Agricolas de plantaciones y boques inducidos), 39.29% (Vegetacion Halofila Hidrofila con mayores confusiones con Suelos Desnudos y Pastizales), 50.62% (Pastizales con mayores confusiones con Tierras Agricolas) y 57.90% (Suelo Desnudo con mayores confusiones con Tierras Agricolas y Urbano y Construido) "

echo $name
echo $clases
echo $1
echo $2

/home/geonode_user/.local/bin/import_raster --base_directory $1 --input_filename $2 --region "$region" --name "$name" --title "$title" --abstract "$abstract" --key_words "$kw"
```


Command lines to register:

```
bash register_TNC_rasters.sh /LUSTRE/MADMEX/tnc_data_steffen_thilo/tnc_marismas/ marismasnacionales_coberturadesuelo_2019_nivel2_final_20190925.tif
```

# Create downloadable links for rasters:

## Note: this next execution use recent implementation of geonode_conabio_package

Shell script:

`create_downloadable_links_in_geonode.sh`

```
#!/bin/bash

#title of layer already registered in geonode in $1
#nocmap in $2 if passed then dont write cmap in raster

dir_path_styles="/LUSTRE/MADMEX/geonode_spc_volume/geonode/scripts/spcgeonode/_volume_geodatadir/workspaces/geonode/styles"
dir_path_layers="/LUSTRE/MADMEX/geonode_spc_volume/geonode/scripts/spcgeonode/_volume_geodatadir/data/geonode/"
download_path_ftp="ftp://geonode.conabio.gob.mx/pub"
destiny_path="/data/var/ftp/pub/"

create_download_link_in_geonode_for_raster --title_layer "$1" --destiny_path $destiny_path --dir_path_styles_geonode $dir_path_styles --dir_path_layers_geonode $dir_path_layers --download_path $download_path_ftp $2
```

```
bash create_downloadable_links_in_geonode.sh "Cobertura de suelo TNC marismas nacionales 2018, 2019 13 clases"
```