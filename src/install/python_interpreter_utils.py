"""
src/install/python_interpreter_utils.py
Este módulo proporciona utilidades para la gestión de entornos 
Python y la verificación de la configuración de pipenv.
"""

import os
import glob
import sys
import subprocess

class PythonInterpreterUtils:
    """
    Clase que proporciona utilidades para la gestión de intérpretes de Python
    y la verificación de pipenv.
    """

    @staticmethod
    def is_pipenv_updated(python_executable: str) -> bool:
        """
        Verifica si pipenv está actualizado con Pipfile y Pipfile.lock.
        
        :param python_executable: Ruta del intérprete de Python a utilizar.
        :return: True si pipenv está actualizado, False en caso contrario.
        """
        print("Verificando si pipenv está actualizado...")
        try:
            result = subprocess.run(
                [python_executable, '-m', 'pipenv', 'sync', '--dry-run'],
                capture_output=True,
                text=True,
                check=True
            )
            if result.returncode == 0:
                print("pipenv está actualizado.")
                return True
            print("pipenv no está actualizado.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error al verificar pipenv. Error: {e}")
            return False

    @staticmethod
    def list_python_interpreters():
        """
        Lista los intérpretes de Python instalados en el sistema, eliminando duplicados.
        
        :return: Lista de rutas a los intérpretes de Python encontrados.
        """
        possible_locations = []
        if os.name == "nt":  # Windows
            possible_locations += glob.glob("C:\\Python*\\python.exe")
            possible_locations += glob.glob("C:\\Users\\*\\"
                                            "AppData\\Local\\Programs\\" 
                                            "Python\\Python*\\python.exe")
        else:  # Unix-based systems
            possible_locations += glob.glob("/usr/bin/python*")
            possible_locations += glob.glob("/usr/local/bin/python*")
            possible_locations += glob.glob("/opt/*/bin/python*")
        python_paths = set()  # Utilizamos un set para eliminar duplicados
        python_paths.add(os.path.normcase(os.path.normpath(sys.executable)))
        for path in possible_locations:
            normalized_path = os.path.normcase(os.path.normpath(path))
            if os.path.exists(normalized_path):
                python_paths.add(normalized_path)
        return sorted(python_paths)
