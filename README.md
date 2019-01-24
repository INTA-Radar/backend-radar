# backend-radar
Aplicación para la gestión de procesos que alimentan la web de radares INTA
Este software permite gestionar _**radares**_ de los cuales se requieren obtener _**productos**_. Los productos posibles a generar son todos los
que se encuentren disponibles en [radar-cmd](https://github.com/INTA-Radar/radar-cmd).

## Dependencias 

1. [radar-cmd](https://github.com/INTA-Radar/radar-cmd)
2. [ftp](https://packages.ubuntu.com/bionic/ftp)  
3. [ruamel](https://pypi.org/project/ruamel.yaml/)
4. [pexpect](https://pypi.org/project/pexpect/)
5. [crontab](https://pypi.org/project/crontab/)

## Uso
Dentro de la carpeta raiz se encuentra un archivo de configuración _**confs.yml**_ en el 
cual se deben establecer las siguientes propiedades:
1. products_yml_dir: carpeta donde se encuentran los archivos yml 
con la configuración de los productos a generar. El nombre de estos archivos
**siempre** debe tener el formato `radar_prod_*.yml` donde en lugar del asterisco
se puede poner el nombre que se requiera. 
En estos archivos se establecen los parametros del producto a generar:
    1. id: identificador del producto, debe ser un numero y en caso de existir 2 o mas
    productos con el mismo identificador solamente se tomara el primero encontrado.
    
    2. Parámetros para `radar-cmd.py`: se deben establecer todos los parámetros necesarios
    para indicar a radar-cmd como debe ser el producto a generar. **NO** deben indicarse los parámetros -f y -do, estos 
    serán establecidos por `backend`.
    
    3. radares: lista de radares a los que se debe ir a buscar el volumen para
    generar el producto. Esta lista debe contener los ID's de los radares configurados (ver punto 2).
    
    4. step: frecuencia (en minutos) con la que se debe generar el producto.
    
    5. active: si el producto se encuentra activo o no. Si se indica `false` se desactiva. 
2. radars_yml_dir: directorio donde se encuentran los archivos yml de los radares disponibles.
Se deben establecer las siguientes propiedades:
    1. id: identificador del radar, es una cadena de texto y no debe repetirse.
    2. host: direccion IP del radar.
    3. port: puerto FTP.
    4. user: usuario FTP
    5. password: contraseña FTP
    6. vols_dir: camino absoluto al directorio donde se encuentran los archivos de radar. 
    
3. tmp_download_dir: directorio de descarga temporal de archivos de radar.
4. products_out_dir: directorio donde se almacenaran los productos generados.
5. logs_dir: directorio donde se almacenaran los logs de los productos.
6. backend_dir: directorio raíz de `backend-radar`.
7. radar_cmd_dir: directorio raíz de `radar-cmd`.
8. python_bin: directorio donde se encuentra python3, si se establece '' (cadena vacia) se usa 
el configurado por el SO.



Todos los valores deben ser caminos absolutos a las carpetas correspondientes.

