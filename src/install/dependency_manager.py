"""
src/install/dependency_manager.py
Este módulo proporciona clases para la gestión de dependencias, incluyendo la actualización de pip,
la instalación de dependencias y la verificación de dependencias faltantes.
"""

import subprocess
import sys
from abc import ABC, abstractmethod

class Updater(ABC):
    """
    Interfaz para actualizadores. Define el método `update` que debe ser implementado
    por las subclases.
    """
    @abstractmethod
    def update(self) -> None:
        """Actualiza alguna herramienta o dependencia."""
        print("Actualizando...")



class PipUpdater(Updater):
    """
    Clase responsable de actualizar pip a la última versión disponible.
    Implementa la interfaz `Updater`.
    """
    def update(self) -> None:
        """
        Actualiza pip utilizando el comando `pip install --upgrade pip`.
        """
        print("Actualizando pip...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            print("pip actualizado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"No se pudo actualizar pip. Error: {e}")


class DependencyInstaller(ABC):
    """
    Interfaz para la instalación de dependencias.
    Las clases que hereden de esta deberán implementar el método `install`.
    """
    @abstractmethod
    def install(self, dependency: str) -> bool:
        """Instala una dependencia."""
        print(f"Instalando {dependency}...")


class PipDependencyInstaller(DependencyInstaller):
    """
    Clase concreta que implementa la instalación de dependencias usando pip.
    Implementa la interfaz `DependencyInstaller`.
    """
    def install(self, dependency: str) -> bool:
        """
        Instala una dependencia usando pip.

        :param dependency: Nombre de la dependencia a instalar.
        :return: True si la instalación fue exitosa, False en caso contrario.
        """
        print(f"Instalando {dependency} usando pip...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
            print(f"{dependency} instalado correctamente.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"No se pudo instalar {dependency}. Error: {e}")
            return False


class DependencyInstallerManager:
    """
    Clase responsable de instalar las dependencias faltantes.
    Ahora depende de interfaces en lugar de clases concretas.
    """
    def __init__(self, installer: DependencyInstaller, updater: Updater, max_retries: int = 3):
        """
        Inicializa la clase DependencyInstallerManager con un instalador y un actualizador.

        :param installer: Instancia de una clase que implementa la interfaz DependencyInstaller.
        :param updater: Instancia de una clase que implementa la interfaz Updater.
        :param max_retries: Número máximo de intentos para instalar cada dependencia.
        """
        self.installer = installer
        self.updater = updater
        self.max_retries = max_retries

    def install_missing_dependencies(self, requirements_file: str = 'requirements.txt') -> None:
        """
        Instala las dependencias faltantes utilizando el instalador proporcionado.
        Si una instalación falla, se reintentará hasta max_retries veces.

        :param requirements_file: Ruta al archivo requirements.txt que contiene las dependencias.
        """
        failed_dependencies = []  # Lista para almacenar dependencias que no se pudieron instalar

        print(f"Leyendo dependencias desde {requirements_file}...")

        try:
            with open(requirements_file, 'r', encoding='utf-8') as file:
                dependencies = file.read().splitlines()
        except FileNotFoundError:
            print(f"El archivo {requirements_file} no fue encontrado.")
            return

        print(f"Las siguientes dependencias están faltantes: {', '.join(dependencies)}")
        print("Intentando instalar dependencias faltantes...")

        for dep in dependencies:
            success = False
            for attempt in range(self.max_retries):
                print(f"Intentando instalar {dep} (intento {attempt + 1}/{self.max_retries})...")
                if self.installer.install(dep):
                    success = True
                    break
                print(f"Reintentando instalación de {dep}...")

            if not success:
                print(f"Fallo la instalación de {dep} después de {self.max_retries} intentos.")
                failed_dependencies.append(dep)

        if failed_dependencies:
            print("Las siguientes dependencias no pudieron ser instaladas:")
            print(", ".join(failed_dependencies))
        else:
            print("Todas las dependencias fueron instaladas exitosamente.")
