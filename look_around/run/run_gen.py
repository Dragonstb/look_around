from pathlib import Path
from project import Project


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
    # print('cwd: '+str(Path.cwd().absolute()))
    # print('new: '+str(Path(Path.cwd().absolute(), name)))
    # try:
    #     with open('file.txt', 'wt') as f:
    #         f.write('Hello World\n')
    # except BaseException as be:
    #     print('oooops')
