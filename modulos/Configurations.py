import os,logging
import yaml

def getLog(name,filename):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.INFO)


    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    fh.setFormatter(formatter)
    # add the handlers to logger

    logger.addHandler(fh)
    return logger


def getConfsValue(key):
    abspath = os.path.abspath(__file__)

    with open(os.path.dirname(abspath)+'/../confs.yml', 'r') as stream:
        try:
            confs = yaml.load(stream)
            return confs[key]
        except yaml.YAMLError as exc:
            print(exc)
