"""
src/install/project_name_utils.py
Este módulo proporciona la clase ProjectNameRetriever, 
que es responsable de obtener el nombre del proyecto
basado en el nombre del directorio principal.
"""

from pathlib import Path

class ProjectNameRetriever:
    """
    Clase responsable de obtener el nombre del proyecto basado en el nombre del directorio principal 
    o un archivo específico.
    """
    def __init__(self, project_dir: Path = None):
        """
        Inicializa la clase con la ruta del directorio del proyecto.
        
        :param project_dir: Ruta del directorio del proyecto.
        """
        self.project_dir = project_dir or Path.cwd()

    def get_project_name(self) -> str:
        """
        Recupera el nombre del proyecto basado en el nombre del directorio principal.

        :return: Nombre del proyecto.
        """
        try:
            project_name = self.project_dir.name
            return project_name
        except AttributeError as e:
            print(f"Error al obtener el nombre del proyecto: {e}")
            return "Unknown_Project"

    def get_project_name_from_file(self, file_name: str) -> str:
        """
        Recupera el nombre del proyecto desde un archivo específico.

        :param file_name: Nombre del archivo que contiene el nombre del proyecto.
        :return: Nombre del proyecto.
        """
        file_path = self.project_dir / file_name
        return file_path.read_text().strip()
    