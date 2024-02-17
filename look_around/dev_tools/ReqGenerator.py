import numpy as np
import numpy.typing as npt
import company_gen
from job_exp_gen import JobExpGen as JEG
import utils
from typing import List

# experience discriminators
_min_quantifiers = np.array(['at least', 'minimum', 'not less than'])
_qualifiers = np.array(['first', 'profound', 'sound'])
_numbers = np.array(['one', 'two', 'three', 'four',
                     'five', 'six', 'seven', 'eight', 'nine'])
_xp = np.array(['experience in', 'knowledge of'])


class ReqGenerator:

    rand = np.random.default_rng()
    company_name: str
    company_desc: str
    job_exp: List[str]

    def __init__(self) -> None:
        self.company_name = company_gen.gen_company_name()
        self.company_desc = company_gen.gen_company_desc(self.company_name)

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
