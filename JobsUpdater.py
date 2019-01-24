from crontab import CronTab
from modulos.Agenda import Agenda
import re
import argparse
from modulos.Configurations import getConfsValue

parser = argparse.ArgumentParser(description='Procesamiento de productos.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-u', type=str, required=True,
                    help='Usuario del SO donde se registraran los crones.')


args = vars(parser.parse_args())


cron = CronTab(user=args['u'])
radar_job_name = re.compile('^backend_radar_job.*')
ag = Agenda(getConfsValue('products_yml_dir'))
ag.loadProducts()

jobs_croned = set()
for job in cron:
    if len(radar_job_name.findall(job.comment)) == 1:
        id_product = job.comment.split(' ')[1]
        jobs_croned.add(int(id_product))

# Agrego nuevos productos
products = set(ag.getProductsId())
not_croned = products.difference(jobs_croned)

for id_nc in not_croned:

    prod = ag.getProduct(id_nc)
    print('Agregando producto ' + str(prod.id))

    job = cron.new(command=getConfsValue('python_bin')+'python3 '+getConfsValue('backend_dir')+'backend.py -p '+str(id_nc), comment='backend_radar_job '+str(id_nc))
    job.minute.every(prod.step)
    job.enable(prod.active)

    #ag.setNotChanged(prod.id)

update = products.difference(not_croned)

for prod_id in update:
    prod = ag.getProduct(prod_id)
    print('Actualizando producto ' + str(prod.id))
    found = [job for job in cron.find_comment('backend_radar_job '+str(prod.id))]
    if len(found) == 1:
        job = found[0]
        job.minute.every(prod.step)
        job.enable(prod.active)
        #ag.setNotChanged(prod.id)
    else:
        raise Exception('Hay mas de un job con el mismo comentario')

removed = jobs_croned.difference(products)

for id_rem in removed:
    print('Borrando producto ' + str(id_rem))
    found = [job for job in cron.find_comment('backend_radar_job ' + str(id_rem))]
    if len(found) == 1:
        job = found[0]
        job.delete()
    else:
        raise Exception('Hay mas de un job con el mismo comentario')

cron.write()
