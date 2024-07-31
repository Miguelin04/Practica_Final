class Binary:
    def binary_primitive(self, array, data, low, high):
        while low <= high:
            mid = (low + high) // 2
            if array[mid] == data:
                return mid
            elif array[mid] < data:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def binary_string(self, array, data, low, high):
        while low <= high:
            mid = (low + high) // 2
            if array[mid].lower().endswith(data.lower()):
                return mid
            elif array[mid].lower() < data.lower():
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def search_models(self, array, element, attribute, low, high, method='binary'):
        if method == 'binary':
            while low <= high:
                mid = (low + high) // 2
                mid_value = getattr(array[mid], attribute)
                if attribute == '_dia':
                    search_value = str(element)
                else:
                    try:
                        search_value = float(element)
                    except ValueError:
                        search_value = str(element)

                if mid_value == search_value:
                    return array[mid]
                elif mid_value < search_value:
                    low = mid + 1
                else:
                    high = mid - 1
            return None
        elif method == 'sequential':
            pass
        else:
            raise ValueError("Método de búsqueda no válido. Debe ser 'binary' o 'sequential'.")
