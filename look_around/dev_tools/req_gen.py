import numpy as np
import numpy.typing as npt
from dev_tools import company_gen
from dev_tools.job_exp_gen import JobExpGen as JEG
from dev_tools.job_task_gen import JobTaskGen as JTG
from dev_tools.job_ben_gen import JobBenGen as JBG
from dev_tools import utils

_exp_headers = np.array([
    'Required experience:',
    'What you have done already:',
    'Your knowledge:',
    'Your skills:'
])

_task_headers = np.array(
    ['On this job, you will', 'Your tasks:', 'What you are going to achieve'])

_bens_headers = np.array([
    'Our benefits:', 'You can expect:', 'We offer:'
])

# skills
_exp_db = np.array(['CouchDB', 'MongoDB', 'PostgreSQL',
                   'MySQL', 'MariaDB', 'SQL', 'NoSQL'])
_exp_dwh = np.array(['Data Warehouses', 'Data Lakes', 'PaaS', 'Snowflake'])
_exp_cloud = np.array(
    ['AWS', 'Google Cloud', 'MS Azure', 'OpenStack', 'IBM Cloud'])
_exp_ds_python = np.array(
    ['NumPy', 'Pandas', 'PyTorch', 'Scikit-learn', 'Matplotlib', 'SciPy', 'Tensorflow/Keras'])
_exp_ml = np.array(['machine learning', 'regression', 'categorization', 'decision trees', 'clustering',
                   'convolutional neural networks', 'recurrent neural networks', 'NLP', 'generative AI'])
_exp_langs = np.array(['Python', 'C', 'C++', 'Java',
                      'C#', 'Node JS', 'php', 'Fortran 77', 'R'])
_exp_progpipes = np.array(['CI/CD', 'unit tests', 'integration tests',
                          'software testing', 'Docker', 'Software Containers'])
_exp_webfws = np.array(['JavaEE', 'Spring', 'Spring Boot', 'Angular', 'React'])
_exp_bi = np.array(['Power BI', 'Tableau'])
_exp_processes = np.array(
    ['Data Mining', 'Process Mining', 'process engineering', 'process definition', 'MS Visio', 'PM tools',
     'project management', 'KPIs', 'OKRs'])

# jobs
_Data_Eng = 'Data Engineer'
_Data_Sci = 'Data Scientist'
_Data_Ana = 'Data Analyst'
_Web_Dev = 'Web Developer'
_Back_Dev = 'Backend Developer'
_IT_Cons = 'IT Consultant'

_jobs = np.array([_Data_Eng, _Data_Sci, _Data_Ana,
                 _Web_Dev, _Back_Dev, _IT_Cons])

_skills = {
    _Data_Eng: np.concatenate([_exp_db, _exp_cloud, _exp_langs, _exp_dwh]),
    _Data_Sci: np.concatenate(
        [_exp_cloud, _exp_ml, _exp_langs, _exp_ds_python]),
    _Data_Ana: np.concatenate([_exp_ml, _exp_ds_python, _exp_db, _exp_bi]),
    _Web_Dev: np.concatenate([_exp_langs, _exp_webfws, _exp_progpipes]),
    _Back_Dev: np.concatenate(
        [_exp_langs, _exp_webfws, _exp_db, _exp_progpipes]),
    _IT_Cons: np.concatenate([_exp_processes, _exp_bi, _exp_db])
}


class ReqGen:
    """
    Creates a random job requisition.
    """

    rand: np.random.Generator
    company_name: str
    company_loc: str
    company_desc: str
    job_name: str
    exp_header: str
    job_exp: npt.NDArray[np.str_]
    task_header: str
    job_tasks: npt.NDArray[np.str_]
    bens_header: str
    job_bens: npt.NDArray[np.str_]

    def __init__(self, location: str = 'Hometown') -> None:
        self.rand = np.random.default_rng()
        self.redesign(location)

    def redesign(self, location: str = 'Hometown') -> None:
        # company
        self.company_name = company_gen.gen_company_name()
        self.company_desc = company_gen.gen_company_desc(self.company_name)
        self.company_loc = location

        # job
        self.job_name = utils.pick_from_array(_jobs)
        level = self.rand.integers(3)

        if level == 0:
            min = 3
            max = 5
        elif level == 1:
            min = 4
            max = 7
        else:
            min = 5
            max = 8

        # tasks done on this job
        self.task_header = utils.pick_from_array(_task_headers)
        roll = self.rand.integers(min, max)
        self._pick_tasks(roll)

        # required experience
        self._pick_exp_header()
        roll = self.rand.integers(min, max)
        self._pick_exp(_skills[self.job_name], roll)

        # level, part 2
        if level == 0:
            self.job_name = 'Junior '+self.job_name
        elif level == 2:
            self.job_name = 'Senior '+self.job_name

        # benefits
        self.bens_header = utils.pick_from_array(_bens_headers)
        roll = self.rand.integers(2, 8)
        self._pick_bens(roll)

    # _______________ company _______________

    def get_company_name(self) -> str:
        """
        Gets the company name.

        returns:
        The company name stored in thsi instance.
        """
        return self.company_name

    def get_company_description(self) -> str:
        """
        Gets the company description.

        returns:
        The self desription of the company.
        """
        return self.company_desc

    # _______________ job _______________

    def _pick_exp_header(self) -> None:
        self.exp_header = utils.pick_from_array(_exp_headers)

    def _pick_exp(self, skills: npt.NDArray[np.str_], size: int = 1) -> None:
        jeg = JEG()
        self.job_exp = np.array(
            [jeg.gen_experience_line(skills) for _ in range(size)])
        pass

    def _pick_tasks(self, size: int = 1) -> None:
        jtg = JTG()
        self.job_tasks = np.array([jtg.gen_job_task() for _ in range(size)])

    def _pick_bens(self, size: int = 1) -> None:
        jbg = JBG()
        self.job_bens = jbg.gen_benefits(size, size)

    # _______________ utilities _______________

    def get_html(self) -> str:
        """
        Generates a simple html page which displays the job requisition.

        returns:
        Html code for the page with the requisition.
        """
        h2s = '<h2>'
        h2e = '</h2>'
        ps = '<p>'
        pe = '</p>'
        ds = '<div>'
        de = '</div>'
        uls = '<ul>'
        ule = '</ul>'
        lis = '<li>'
        lie = '</li>'
        page = []

        page.append('<!DOCTYPE html>')
        page.append('<html lang="en">')
        page.append('<head>')
        page.append('<meta charset="UTF-8">')
        page.append('<title>'+self.job_name+' - '+self.company_name+'</title>')
        page.append('</head>')
        page.append('<body>')

        page.append('<h2 id="job_name">')
        page.append(self.job_name)
        page.append(h2e)
        page.append(ps)
        page.append(ds)
        page.append(self.company_name)
        page.append(de)
        page.append('<div id="company_location">')
        page.append(self.company_loc)
        page.append(de)
        page.append(pe)
        page.append('<p id="company_description">')
        page.append(self.company_desc)
        page.append(pe)
        page.append(ps)
        page.append(ds)
        page.append(self.task_header)
        page.append(de)
        page.append('<ul id="job_tasks">')
        [page.append(lis+task+lie) for task in self.job_tasks]
        page.append(ule)
        page.append(pe)

        page.append(ps)
        page.append(ds)
        page.append(self.exp_header)
        page.append(de)
        page.append('<ul id="job_experience">')
        [page.append(lis+exp+lie) for exp in self.job_exp]
        page.append(ule)
        page.append(pe)

        page.append(ps)
        page.append(ds)
        page.append(self.bens_header)
        page.append(de)
        page.append('<ul id="job_benefits">')
        [page.append(lis+bens+lie) for bens in self.job_bens]
        page.append(ule)
        page.append(pe)

        page.append('</body>')
        page.append('</html>')

        return ''.join(page)

    def print(self) -> None:
        """
        Prints the job requisition to the console.
        """
        print()
        print(self.job_name)
        print()
        print(self.company_name)
        print(self.company_loc)
        print()
        print(self.company_desc)
        print()
        print(self.task_header)
        [print('\t'+task) for task in self.job_tasks]
        print()
        print(self.exp_header)
        [print('\t'+experience) for experience in self.job_exp]
        print()
        print(self.bens_header)
        [print('\t'+ben) for ben in self.job_bens]
        print()
