# -*- coding: utf-8 -*-

__author__ = "Andres Giordano"
__version__ = "0.1.0"
__maintainer__ = "Andres Giordano"
__email__ = "andresgiordano.unlu@gmail.com"
__status__ = "Testing"

from modulos.RadarFT import RadarFT
from modulos.Agenda import Agenda
from modulos.RadarManager import RadarManager
import os
import argparse
import datetime
import subprocess

from modulos.Configurations import getLog,getConfsValue

# Cambio directorio de trabajo al directorio de este script porque  es ejecutado desde un Cron

parser = argparse.ArgumentParser(description='Procesamiento de productos.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-p', type=int, required=True,
                    help='Producto a procesar.')


args = vars(parser.parse_args())

def cleanTemp():
    if len(files)>0:
        logger.info('Borrando archivos temporales')
        # Borrando los archivos una vez generado el producto
        for f in files:
            os.remove(f)

rm = RadarManager(getConfsValue('radars_yml_dir'))
rm.loadRadars()
ag = Agenda(getConfsValue('products_yml_dir'))
ag.loadProducts()

prod = ag.getProduct(args['p'])

abspath = os.path.abspath(__file__)
logger = getLog('backend_logger', getConfsValue('logs_dir')+'backend_log_product_' + str(prod.id))

all_vol_found = True
files = []

# Si no existe la carpeta de descarga para este producto se crea
prod_download_dir = getConfsValue('tmp_download_dir')+str(prod.id)
if not os.path.isdir(prod_download_dir):
    os.mkdir(prod_download_dir)

prod_out_dir = getConfsValue('products_out_dir')+str(prod.id)
if not os.path.isdir(prod_out_dir):
    os.mkdir(prod_out_dir)
prod_out_dir += '/'

for r_id in prod.radares:

    logger.info('Generando producto '+str(prod.id)+ ' para radar '+r_id)

    # Si no existe la carpeta de descarga para el radar se crea dentro de la del producto
    radar_download_dir = prod_download_dir + '/'+r_id
    if not os.path.isdir(radar_download_dir):
        os.mkdir(radar_download_dir)

    radar_download_dir += '/'

    radar = rm.getRadar(r_id)
    radar_ft = RadarFT(radar)
    if radar_ft.isConnected():
        start_time = datetime.datetime.today() - datetime.timedelta(minutes = prod.step)

        file = radar_ft.searchVol(int(start_time.strftime("%H")),
                                  int(start_time.strftime("%M")),
                                  prod.var,
                                  prod.step)

        if file is not None:
            logger.info('Volumen encontrado: '+file)
            out_filename = radar_download_dir+file
            logger.info('Guardando en: ' + out_filename)
            radar_ft.downloadVolFile(file, out_filename)
            files.append(out_filename)
        else:
            logger.warn('No se encontro el volumen')
            all_vol_found = False

    else:
        logger.error('No se logro conectar al radar '+r_id)

if prod.m and not all_vol_found:
    logger.warn('No se puede generar el mosaico porque no fueron encontrados todos los volumenes.')
    cleanTemp()
    exit(0)

# Genero el producto
if len(files)>0:
    radar_cmd_command = getConfsValue('python_bin')+'python3 '+getConfsValue('radar_cmd_dir')+'radar-cmd.py -pf ' + prod.file + ' -f '+','.join(files)+ ' -do '+getConfsValue('products_out_dir')
    logger.info(radar_cmd_command)
    res = subprocess.call(radar_cmd_command, shell=True)
    logger.info('radar-cmd exit('+str(res)+')')
    cleanTemp()
else:
    logger.warn('Sin archivos para generar el producto.')
