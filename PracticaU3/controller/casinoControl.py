from controller.dao.daoAdapter import DaoAdapter
from models.casino import Casino

class CasinoControl(DaoAdapter):
    def __init__(self):
        super().__init__(Casino)
        self.__casino = None

    @property
    def _casino(self):
        if self.__casino == None:
            self.__casino = Casino()
        return self.__casino

    @_casino.setter
    def _casino(self, value):
        self.__casino = value

    def _lista(self):
        return self._list()

    @property
    def save(self):
        self._save(self._casino)
        
    def merge(self, pos):
        self._merge(self._casino, pos)
    
    def delete(self, pos):
        self._delete(self._casino,pos)
    
    def sort_models(self, campo_orden, direccion, algoritmo):
        linked_list = self._list()
        linked_list.sort_models(campo_orden, direccion, algoritmo)
        return linked_list.toArray