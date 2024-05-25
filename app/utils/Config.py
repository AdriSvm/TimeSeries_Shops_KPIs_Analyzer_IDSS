"""
Main class for managing the configuration files
Steps to use it:
    1. Create a file with the configuration data in JSON format.
    2. Create an instance of Config with the path to the file.
    3. Use the attributes of the instance to access the data. If the attribute does not exist, returns None.
    4. Use the data as needed.
    5. Profit.
Example:
    config = Config('config.json')
    print(config.api_key)
    print(config.api_secret)
    print(config.api_url)
    print(config.api_version)
    print(config.non_existent_attribute)  # Returns None

"""

import json

class Config:
    def __init__(self, filepath):
        self._data = {}
        try:
            with open(filepath, 'r') as file:
                self._data = json.load(file)
        except FileNotFoundError:
            print(f"El archivo {filepath} no fue encontrado.")
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON en el archivo {filepath}.")

    def __getattr__(self, name):
        # Este método se llama si no se encuentra el atributo de manera regular.
        # Buscamos el nombre del atributo en los datos cargados.
        # Si el atributo no existe, se devuelve None.
        return self._data.get(name, None)

    def __str__(self):
        return str(self._data)
