import pexpect

class LinuxFTPWrapper(object):

    def __init__(self,hostname,user,password,port=21):
        self.__hostname = hostname
        self.__user = user
        self.__password = password
        self.__port = port
        self.__ftpSession = None


    def __delete__(self, instance):
        self.__ftpSession.close()

    def __writeCommand(self,cmd):
        self.__ftpSession.sendline(cmd)
        self.__ftpSession.expect('ftp> ')

    def connect(self):
        self.__ftpSession = pexpect.spawnu('ftp -ni ' + self.__hostname, echo=False)
        self.__ftpSession.expect('ftp> ')

        if self.__ftpSession.before.strip() == 'ftp: connect: No route to host':
            return False
        # TODO faltan mas verificaciones para saber si se pudo conectar correctamente
        self.__writeCommand('verbose')
        self.__writeCommand('quote USER ' + self.__user)
        self.__writeCommand('quote PASS ' + self.__password)

        return True

    def execute(self,cmd):
        self.__writeCommand(cmd)

    def getResponse(self):
        return self.__ftpSession.before
