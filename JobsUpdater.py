from crontab import CronTab
from modulos.Agenda import Agenda
import re

cron = CronTab(user='andres')
radar_job_name = re.compile('^backend_radar_job.*')
ag = Agenda('../products')
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

    job = cron.new(command='~/radar_wrap_p3/bin/python3 ~/PycharmProjects/backend-radar/backend.py -p '+str(id_nc), comment='backend_radar_job '+str(id_nc))
    job.minute.every(prod.step)
    job.enable(prod.active)

    ag.setNotChanged(prod.id)

for prod in ag.getChangedProducts():
    print('Actualizando producto ' + str(prod.id))
    found = [job for job in cron.find_comment('backend_radar_job '+str(prod.id))]
    if len(found) == 1:
        job = found[0]
        job.minute.every(prod.step)
        job.enable(prod.active)
        ag.setNotChanged(prod.id)
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
