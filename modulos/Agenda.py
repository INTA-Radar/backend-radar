import ruamel.yaml
import glob, os

class Product:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Agenda(object):

    def __init__(self, products_dir):
        self.__products = {}
        self.__products_dir = products_dir


    def loadProducts(self):
        """
        Carga los productos que se encuentran en el directorio de productos.

        :return:
        """

        for file in glob.glob(self.__products_dir+"/radar_prod_*.yml"):
            with open(file, 'r') as stream:
                try:
                    yaml = ruamel.yaml.YAML()
                    prod = yaml.load(stream)

                    prod['file'] = os.path.join(self.__products_dir,file)
                    prod_id = prod['id']
                    if prod_id not in self.__products:
                        self.__products[prod_id] = Product(**prod)
                    else:
                        raise Exception('Ya existe un producto registrado con ID = '+ str(prod['id']))
                except Exception as exc:
                    print(exc)

    def getProductsId(self):

        return self.__products.keys()

    def getProduct(self, id_prod):
        """
        Devuelve un producto por ID.

        :param id_prod: id del producto
        :type id_prod: int
        :return:
        """
        return self.__products[id_prod]