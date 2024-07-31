from numbers import Number
from controller.tda.linked.node import Node
from controller.exception.linkedEmpty import LinkedEmpty
from controller.exception.arrayPositionException import ArrayPositionException
from controller.tda.linked.order.mergeSort import MergeSort
from controller.tda.linked.order.shellSort import ShellSort
from controller.tda.linked.order.quickSort import QuickSort
from controller.tda.linked.search.binarySecuencial import BinarySecuencial
from controller.tda.linked.search.binary import Binary
class Linked_List(object):

    def __init__(self):
        self.__head = None
        self.__last = None
        self.__length = 0

    @property
    def _length(self):
        return self.__length

    @_length.setter
    def _length(self, value):
        self.__length = value
 
        
    @property    
    def isEmpty(self):
        return self.__head == None or self._length == 0
    
    def _getFirst_(self, poss):
        if not self.isEmpty:
            return self.__head
        else:
            return "List is Empty"
    
    def _getLast_(self, poss):
        if not self.isEmpty:
            return self.__last
        else:
            return "List is Empty"
        

    def getNode(self, poss): #DEVUELVE DATA 
        if self.isEmpty:
           raise LinkedEmpty("List is Empty")
        elif poss < 0 or poss >= self.__length:
            raise ArrayPositionException("Index out of range")
        elif poss == 0:
            return self.__head._data
        elif poss == (self.__length - 1):
            return self.__last._data
        else:
            node = self.__head
            cont = 0
            while cont < poss:
                cont += 1
                node = node._next
            return node._data
        
    def get(self, poss): #DEVUELVE EL NODO
        if self.isEmpty:
           raise LinkedEmpty("List is Empty")
        elif poss < 0 or poss >= self.__length:
            raise ArrayPositionException("Index out of range")
        elif poss == 0:
            return self.__head
        elif poss == (self.__length - 1):
            return self.__last
        else:
            node = self.__head
            cont = 0
            while cont < poss:
                cont += 1
                node = node._next
            return node
            
    def addFirst(self, data):
        if self.isEmpty:
            node = Node(data)
            self.__head = node
            self.__last = node
            self.__length += 1
        else:
            headOld = self.__head #guarada toda la lista hara ahora
            node = Node(data, headOld)  
            self.__head = node
            self.__length += 1

    def addLast(self, data):
        if self.isEmpty:
            self.addFirst(data)
        else:
            node = Node(data)
            self.__last._next = node 
            self.__last = node
            self.__length += 1

    
    def addNode(self, data, poss = 0):
        if poss == 0:
            self.addFirst(data)
        elif poss == self.__length:
            self.addLast(data)
        else:
            node_preview = self.get(poss - 1)
            node_actuality = node_preview._next
            node = Node(data, node_actuality)
            node_preview._next = node
            self.__length += 1
    
    def add(self, data, pos = 0):
        if pos == 0:
            self.addFirst(data)
        elif pos == self.__length:
            self.addLast(data)
        else:
            node_preview = self.get(pos - 1)
            node_last = node_preview._next #self.getNode(pos)
            node = Node(data, node_last)
            node_preview._next = node
            self.length += 1


    def edit (self, data, poss = 0):
        if poss == 0:
            self.__head._data = data
        elif poss == (self.__length - 1):
            self.__last._data = data
        else:
            node = self.get(poss)
            node._data = data


    # @property
    # def toArray (self):
    #     array = TDAArray(self.__length)
    #     if not self.isEmpty:
    #         node = self.__head
    #         cont = 0
    #         while cont < self.__length:
    #             array.insert(node._data, cont) #array[cont] = node._data
    #             cont += 1
    #             node = node._next
    #     return array
    
    @property
    def toArray(self):
        array = []
        if not self.isEmpty:
            node = self.__head
            cont = 0
            while cont < self._length:
                array.append(node._data)	
                cont += 1
                node = node._next
        return array
        
    def toList(self, array):
        self.clear
        for i in range(0, len(array)):
            self.addLast(array[i])


    def dicToList(self, array_dict):
        for i in range(0, len(array_dict)):
            node = Node(array_dict[i])
            self.addLast(node)
            
    def deleteFirst(self):
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            element = self.__head._data
            aux = self.__head._next
            self.__head = aux
            if self.__length == 1:
                self.__last = None
            self._length = self._length - 1
            return element
        
    def deleteLast(self):
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            element = self.__last._data
            aux = self.get(self._length - 2)

            #self.__head = aux
            if aux == None:
                self.__last = None
                if self.__length == 2:
                    self.__last = self.__head
                else:
                    self.__head = None
            else:
                self.__last = None
                self.__last = aux
                self.__last._next = None
            self._length = self._length - 1
            return element
    
    def delete(self, poss = 0 ):
        if self.isEmpty:
            raise LinkedEmpty("List is Empty")
        elif poss < 0 or poss >= self.__length:
            raise ArrayPositionException("Index out of range")
        elif poss == 0:
            node = self.__head._next
            del self.__head
            self.__head = node
            self.__length -= 1
        elif poss == (self.__length - 1):
            print("entro en el ultimo")
            node = self.getNode(self.__length - 2)
            node._next = None
            del self.__last
            self.__last = node
            self.__length -= 1
            print(self.__length)
        else:
            node_previous = self.getNode(poss-1)
            node_next = node_previous._next._next
            node_previous._next = node_next
            self.__length -= 1
    #serializable
    @property
    def serializable(self):
        array = self.toArray
        array_dict = []
        for i in range(0, len(array)):
            array_dict.append(array[i].__dict__)
        return array_dict
    
    @property
    def clear(self):
        self.__head = None
        self.__last = None
        self.__length = 0

    def __str__(self) -> str: #metodo toString    #cometar ctrl+k+c   / ctrl+k+u
        out = ""
        if self.isEmpty:
            out = "List is Empty"
        else:
            node = self.__head
            while node != None:
                out += str(node._data) + " -> "
                node = node._next
        return out
    
    @property
    def print(self):
        node = self.__head
        data = ""
        while node != None :
            data += str(node._data) + "   "
            node = node._next
        print("Lista de datos")
        print(data)
    # -------------------------------------------Metodos de Ordenacion-------------------------------------------------------------
    
    def sort(self, type, typeSort = 1):
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            array = self.toArray
            if isinstance(array[0], Number) or isinstance(array[0], str):
                if typeSort == 1:
                    order = QuickSort()
                elif typeSort == 2:
                    order = MergeSort()
                else:
                    order = ShellSort()
                if type == 1:
                    array = order.sort_primitive_ascendent(array)
                else:
                    array = order.sort_primitive_descendent(array)
            self.toList(array)

    def sort_models(self, attribute, type = 1, typeSort = 1):
            if self.isEmpty:
                raise LinkedEmpty("List empty")
            else:
                array = self.toArray
                if isinstance(array[0], object):
                    if typeSort == 1:
                        order = QuickSort()
                    elif typeSort == 2:
                        order = MergeSort()
                    else:
                        order = ShellSort()
                    if type == 1:
                        array = order.sort_models_ascendent(array, attribute)
                    else:
                        array = order.sort_models_descendent(array, attribute)
                self.toList(array)
            return self
    # -------------------------------------------Metodos de Busqueda-------------------------------------------------------------

    def search_equals(self, data):
        list = Linked_List()
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            array = self.toArray
            for i in range (0, len(array)):
                if (array[i].lower().__contains__(data.lower())):    
                    list.add(array[i], list._length)
        return list
    
    def binary_search(self, data, type = 1):
        array = self.toArray
        order = QuickSort()
        array = order.sort_primitive_ascendent(array)
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            search = Binary()
            if type == 0:
                return search.binary_string(array, data, 0, len(array) - 1)
            elif type == 1:
                return search.binary_primitive(array, data, 0, len(array) - 1)  
            
                
    def binary_search_models(self, data, attribute, type=1):
        array = self.toArray
        order = ShellSort()
        array = order.sort_models_ascendent(array, attribute)
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            search = Binary()
            result = None
            if type == 1:
                result = search.search_models(array, data, attribute, 0, len(array) - 1)
            elif type == 2:
                result = search.search_models(array, data, attribute, 0, len(array) - 1)
                print(attribute)
            return result

    def binary_models(self, data, attribute, type=1):
        array = self.toArray
        order = QuickSort()
        array = order.sort_models_ascendent(array, attribute)
        if self.isEmpty:
            raise LinkedEmpty("List empty")
        else:
            search = BinarySecuencial()
            if type == 1:
                result = search.binary_models_secuencial(array, data, 0, len(array) - 1, attribute)
                return result
# -------------------------------------------Metodos de Recorrido-------------------------------------------------------------

    def binary_search_models_int(self, data, attribute):
        self.sort_models(attribute)
        arr = self.toArray
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_value = getattr(arr[mid], attribute)
            try:
                mid_value = int(mid_value)
                data = int(data)
            except ValueError:
                return -1  
            
            if mid_value == data:
                return arr[mid]
            elif mid_value < data:
                left = mid + 1
            else:
                right = mid - 1
        return -1
