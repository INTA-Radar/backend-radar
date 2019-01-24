from ftplib import FTP
from .LinuxFTPWrapper import LinuxFTPWrapper
import re
import datetime

class RadarFT(object):

    spaces = re.compile("\s+")
    volfiles = re.compile("\.(azi|vol)$")

    @staticmethod
    def vol_year(vol_name):
        return vol_name[0:4]

    @staticmethod
    def vol_month(vol_name):
        return vol_name[4:6]

    @staticmethod
    def vol_day(vol_name):
        return vol_name[6:8]

    @staticmethod
    def vol_hour(vol_name):
        return vol_name[8:10]

    @staticmethod
    def vol_minutes(vol_name):
        return vol_name[10:12]

    def __init__(self, radar):


        self.__radar = radar

        FTP.debugging = 5
        self.__ftp = LinuxFTPWrapper(self.__radar.host, self.__radar.user, self.__radar.password)
        if self.__ftp.connect():
            self.__ftp.execute('cd '+self.__radar.vols_dir)  #   Se para en el directorio donde se encuentran
                                                                #   los archivos de radar
            self.__connected = True
        else:
            self.__connected = False

    def isConnected(self):
        return self.__connected

    def listRadarFiles(self,pattern=None):

        vol_files = []

        search_str = '{*.vol,*.azi}'
        if pattern is not None:
            search_str = '{'+pattern+'*.vol,'+pattern+'*.azi}'

        self.__ftp.execute('nlist '+search_str)

        for filename in self.__ftp.getResponse().split('\r\n')[:-1]:
            vol_files.append(filename)

        return vol_files

    def searchVol(self,start_hour,start_minute, radarVariable, step,
                        year=datetime.date.today().strftime('%Y'),
                        month=datetime.date.today().strftime('%m'),
                        day=datetime.date.today().strftime('%d')):
        """
        Busca un archivo .vol o .azi en el directorio del radar que manipula el objeto. Se comienza a buscar desde
        `start_hour:start_minute` hasta `start_hour+(step/60):start_minute+(step % 60)`
        TODO en realidad esto deberia recibir como parametro hora/minuto de inicio y de fin de busqueda, no el step

        :param start_hour: hora de comienzo de busqueda del archivo
        :param start_minute: minuto de comienzo de busqueda del archivo
        :param radarVariable:
        :param step:
        :param year:
        :param month:
        :param day:
        :return:
        """
        start_search = datetime.datetime.strptime(day+'-'+month+'-'+year+' '+
                                                  "{:02d}".format(start_hour)+':'+
                                                  "{:02d}".format(start_minute)+':00', '%d-%m-%Y %H:%M:%S')
        for x in range(step):
            end_search = start_search + datetime.timedelta(minutes = x)
            file_to_search = end_search.strftime("%Y%m%d%H%M")+'*'+radarVariable
            radar_files = self.listRadarFiles(pattern=file_to_search)
            if len(radar_files)>0:
                return radar_files[0]

        return None

    def downloadVolFile(self, file, outFile):
        self.__ftp.execute('binary')
        self.__ftp.execute('get '+file+' '+outFile)
        self.__ftp.execute('ascii')
