"""
setup_instalador.py
Setup script for Presupuestador.
"""

import subprocess
import sys
import os
from src.install.dependency_manager import (
    PipUpdater, PipDependencyInstaller, DependencyInstallerManager
)
from src.install.python_interpreter_utils import PythonInterpreterUtils
from src.install.project_installer import ProjectInstaller

def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_mensaje_inicio():
    """Muestra un mensaje inicial indicando el inicio del proceso."""
    print("Iniciando instalador...")

def mostrar_version_python():
    """Imprime la versión actual de Python."""
    print(f"Versión de Python: {sys.version}")

def listar_interpretes_python():
    """Lista los intérpretes de Python disponibles y selecciona uno."""
    python_interpreters = list_python_interpreters()
    print("Intérpretes de Python encontrados:")
    for i, interpreter in enumerate(python_interpreters):
        print(f"[{i}] {interpreter}")
    selected_index = 0
    if selected_index:
        return python_interpreters[int(selected_index)]
    return sys.executable

def actualizar_pip(pip_updater):
    """Actualiza pip utilizando PipUpdater."""
    pip_updater.update_pip()

def verificar_dependencias(installer_manager, requirements_file):
    """Verifica e instala dependencias faltantes desde un archivo requirements."""
    if os.path.exists(requirements_file):
        print(f"Verificando dependencias desde {requirements_file}...")
        installer_manager.install_missing_dependencies(requirements_file)
    else:
        print(f"El archivo {requirements_file} no fue encontrado. ")

def actualizar_pipenv(python_executable):
    """Verifica si pipenv está actualizado y lo actualiza si es necesario."""
    if not is_pipenv_updated(python_executable):
        print("Actualizando dependencias con pipenv...")
        subprocess.check_call([python_executable, '-m', 'pipenv', 'install'])

def instalar_proyecto():
    """Instala el proyecto utilizando ProjectInstaller."""
    project_installer = ProjectInstaller()
    project_installer.main()

def iniciar():
    """Función principal que coordina el proceso de instalación."""
    limpiar_pantalla()
    mostrar_mensaje_inicio()
    mostrar_version_python()

    #python_executable = listar_interpretes_python()

    pip_updater = PipUpdater()
    installer_manager = DependencyInstallerManager(
        PipDependencyInstaller(), pip_updater, max_retries=3
    )

    #actualizar_pip(pip_updater)
    verificar_dependencias(installer_manager, 'requirements.txt')
    #actualizar_pipenv(python_executable)
    instalar_proyecto()

if __name__ == "__main__":
    iniciar()
