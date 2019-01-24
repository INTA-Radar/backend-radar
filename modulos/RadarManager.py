import yaml
import os, glob

class Radar:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class RadarManager(object):

    def __init__(self, radars_dir):

        self.__radars = {}
        self.__radars_dir = radars_dir


    def loadRadars(self):

        for file in glob.glob(self.__radars_dir+"/radar*.yml"):
            with open(file, 'r') as stream:
                try:
                    rad = yaml.load(stream)
                    prod_id = rad['id']
                    if prod_id not in self.__radars:
                        self.__radars[prod_id] = Radar(**rad)
                    else:
                        raise Exception('Ya existe radar registrado con ID = ' + rad['id'])
                except yaml.YAMLError as exc:
                    print(exc)

    def getRadar(self, rad_id):

        return self.__radars[rad_id]