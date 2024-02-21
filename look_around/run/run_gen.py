from pathlib import Path
from run.project import Project


def create_project_folders(name: str, parent: Path) -> Project:
    """
    Creates the pathlib.Path objects of the project.

    name:
    Name of the project.

    parent:
    Directory in which the root directory of the project is created.
    """
    # TODO: check for any file/dir related problems
    prj = Project(name, parent)
    return prj
