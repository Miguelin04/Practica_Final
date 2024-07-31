import random
from typing import List, Any, TypeVar

T = TypeVar('T', int, float)

class QuickSort:
    def sort_primitive_ascendent(self, array: List[T]) -> List[T]:
        if len(array) <= 1:
            return array
        else:
            pivot = array[random.randint(0, len(array) - 1)]
            less = [i for i in array if i < pivot]
            equal = [i for i in array if i == pivot]
            greater = [i for i in array if i > pivot]
            return self.sort_primitive_ascendent(less) + equal + self.sort_primitive_ascendent(greater)

    def sort_primitive_descendent(self, array: List[T]) -> List[T]:
        if len(array) <= 1:
            return array
        else:
            pivot = array[random.randint(0, len(array) - 1)]
            less = [i for i in array if i < pivot]
            equal = [i for i in array if i == pivot]
            greater = [i for i in array if i > pivot]
            return self.sort_primitive_descendent(greater) + equal + self.sort_primitive_descendent(less)

    def sort_models_ascendent(self, array: List[Any], attribute: str) -> List[Any]:
        if len(array) <= 1:
            return array
        else:
            pivot_value = getattr(array[random.randint(0, len(array) - 1)], attribute)
            less = [i for i in array if getattr(i, attribute) < pivot_value]
            equal = [i for i in array if getattr(i, attribute) == pivot_value]
            greater = [i for i in array if getattr(i, attribute) > pivot_value]
            return self.sort_models_ascendent(less, attribute) + equal + self.sort_models_ascendent(greater, attribute)

    def sort_models_descendent(self, array: List[Any], attribute: str) -> List[Any]:
        if len(array) <= 1:
            return array
        else:
            pivot_value = getattr(array[random.randint(0, len(array) - 1)], attribute)
            less = [i for i in array if getattr(i, attribute) < pivot_value]
            equal = [i for i in array if getattr(i, attribute) == pivot_value]
            greater = [i for i in array if getattr(i, attribute) > pivot_value]
            return self.sort_models_descendent(greater, attribute) + equal + self.sort_models_descendent(less, attribute)
