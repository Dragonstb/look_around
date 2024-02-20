import pandas as pd
import math

_Data_Eng = 'Data Engineer'.lower()
_Data_Sci = 'Data Scientist'.lower()
_Data_Ana = 'Data Analyst'.lower()
_Web_Dev = 'Web Developer'.lower()
_Back_Dev = 'Backend Developer'.lower()
_IT_Cons = 'IT Consultant'.lower()

_senior = 'senior'
_junior = 'junior'


def contains(word: str, target: str) -> bool:
    return word.find(target) > -1


class AlgorithmicCategorizer:

    observed: str
    category: int = 0
    pos_mods: int = 0
    neg_mods: int = 0
    reasons: pd.Series
    pop: int = 0

    def __init__(self, observed: str = '', pop: int = 0) -> None:
        self.observed = observed.lower()
        self.pop = pop
        self.reasons = pd.Series(dtype='int64')

    def fit(self, observed: str, town_pop: int) -> None:
        self.set_observed(observed)
        self.pop = town_pop
        self.pos_mods = 0
        self.neg_mods = 0

    def predict(self):
        self.category = 0
        self.reasons = pd.Series(dtype='int64')

        string = self.find_substring('<h2 id="job_name">', '</h2>')
        if len(string) > 0:
            ok = self.analyze_job_name(string)
            if not ok:
                return

        if self.pop > 0:
            self.analyse_population(self.pop)

        string = self.find_substring('<p id="company_description">', '</p>')
        if len(string) > 0:
            self.analyze_job_description(string)

        string = self.find_substring('<ul id="job_tasks">', '</ul>')
        if len(string) > 0:
            self.analyze_tasks(string)

        string = self.find_substring('<ul id="job_experience">', '</ul>')
        if len(string) > 0:
            self.analyze_experiences(string)

        string = self.find_substring('<ul id="job_benefits">', '</ul>')
        if len(string) > 0:
            self.analyze_benefits(string)

        self.evaluate_modificators()

    def set_observed(self, obs: str) -> None:
        self.observed = obs.lower()

    def set_population(self, pop: int) -> None:
        self.pop = pop

    def analyze_job_name(self, name: str) -> bool:
        """
        Analyzes the job name and sets the base category.

        returns:
        Go on with categorization at all?
        """
        # graduation is not too long ago, so Alex avoids seniot positions
        if contains(name, _senior):
            self.category = 0
            self.reasons['base: senior position'] = 0
            return False  # flag: do not continue

        # Data Engineer is what Alex wants to be
        if contains(name, _Data_Eng):
            self.category = 4
            self.reasons['base: Data Engineer'] = 4
        # Data Scientist or Data Analyst is also OK
        elif contains(name, _Data_Sci):
            self.category = 3
            self.reasons['base: Data Scientist'] = 3
        elif contains(name, _Data_Ana):
            self.category = 3
            self.reasons['base: Data Analyst'] = 3
        # Maybe explaining clients who to use data the best way
        elif contains(name, _IT_Cons):
            self.category = 2
            self.reasons['base: IT Consultant'] = 2
        # Web Dev is not really what Alex is looking for
        else:
            self.category = 1
            self.reasons['base: Other'] = 1

        # while looking for junior positions, a job for professionals might fit
        # but is not Alex' main focus
        if name.find(_junior) == -1:
            self.reasons['Not a junior position'] = -1
            self.neg_mods += 1

        return True

    def analyze_job_description(self, desc: str) -> None:
        # Energy and public transport are the fields alex is in
        very_good = ['energy', 'transport']
        good = ['solar energy', 'wind energy',
                'traffic optimization', 'public transport']
        # Alex does not like coal 'cos the parents' house gpt torn down for a coal mine. Somehow, Alex
        # does not like code styles either. Alex is yet young and foolish.
        bad = ['coding styles', 'coal']
        # Alex is not fond of B2B logistics
        very_bad = ['logistics', 'B2B']

        for keyword in very_good:
            if contains(desc, keyword):
                self.pos_mods += 2
                self.reasons['description: '+keyword] = 2
        for keyword in good:
            if contains(desc, keyword):
                self.pos_mods += 1
                self.reasons['description: '+keyword] = 1
        for keyword in bad:
            if contains(desc, keyword):
                self.neg_mods += 1
                self.reasons['description: '+keyword] = -1
        for keyword in very_bad:
            if contains(desc, keyword):
                self.neg_mods += 2
                self.reasons['description: '+keyword] = -2

    def analyze_tasks(self, tasks: str) -> None:
        """
        Looks for the keywords more or less interesting to Alex. The positive and negative modifiers
        are increased accordingly at the presence of such a keyword.
        """
        # Databases draw Alex' interests
        for keyword in ['databases', 'data warehouses', 'data lakes', 'etl pipe lines']:
            if contains(tasks, keyword):
                self.pos_mods += 2
                self.reasons['tasks: '+keyword] = 2

        # working with clients is ok
        for keyword in ['client projects', 'customer projects', 'customers', 'clients']:
            if contains(tasks, keyword):
                self.pos_mods += 1
                self.reasons['tasks: '+keyword] = 1

        # to Alex, most software algorithms are less interesting
        for keyword in ['saas platform', 'software tools', 'algorithms']:
            if contains(tasks, keyword):
                self.neg_mods += 1
                self.reasons['tasks: '+keyword] = -1

    def analyze_experiences(self, exps: str) -> None:
        """
        Analyzeses the required experiences.
        """
        good = ['couchdb', 'mysql', 'mariadb',
                'sql', 'nosql', 'data warehouses', 'openstack', 'data mining', 'tableau', 'python', 'c#', 'node js']
        bad = ['fortran 77', 'javaee', 'spring',
               'spring boot', 'angular', 'react', 'php', 'project management', 'kpis', 'okrs',]
        also_bad = ['five year', 'six year']
        very_bad = ['seven year', 'eight year', 'nine year']

        for keyword in good:
            if contains(exps, keyword):
                self.pos_mods += 1
                self.reasons['expected: '+keyword] = 1
        for keyword in bad:
            if contains(exps, keyword):
                self.neg_mods += 1
                self.reasons['expected: '+keyword] = -1
        for keyword in also_bad:
            if contains(exps, keyword):
                self.neg_mods += 1
                self.reasons['expected: '+keyword+'s experience'] = -1
        for keyword in very_bad:
            if contains(exps, keyword):
                self.neg_mods += 2
                self.reasons['expected: '+keyword+'s experience'] = -2

    def analyze_benefits(self, bens: str) -> None:
        """
        Analyzes the benefits.
        """
        # Alex likes cars as well as bikes. Also a health insurance and a pension pleeds Alex.
        # Free cookies, as always, are out of question
        good = ['company car', 'company bike',
                'health insurance', 'cookie basket', 'pension']

        for keyword in good:
            if contains(bens, keyword):
                self.pos_mods += 1
                self.reasons['benefit: '+keyword] = 1

    def analyse_population(self, population: int) -> None:
        # Alex prefers towns around a million of inhabitants
        if population > 925905 and population < 1200741:
            self.pos_mods += 2
            self.reasons['proper town size'] = 2
        # For some reason, this is a very neat town size to Alex as well
        elif population > 20416 and population < 35840:
            self.pos_mods += 2
            self.reasons['cute town size'] = 2
        # This town size is fair
        elif population > 883014 and population < 1400477:
            self.pos_mods += 1
            self.reasons['fair town size'] = 1
        # The best of all town sizes
        elif population == 1336:
            self.pos_mods += 3
            self.reasons['population is 1336'] = 3
        # far out of range
        elif population < 57240 or population > 3590382:
            self.neg_mods += 2
            self.reasons['awful town size'] = -2
        # Alex feels such towns a bit too empty or too full, respectively
        elif population < 100005 or population > 2005026:
            self.neg_mods += 1
            self.reasons['disturbing town size'] = -1

    def evaluate_modificators(self) -> None:
        """
        Increases the category by unity if the positive modifiers that have arisen from the job requisition
        outweight the negative ones far enough. Likewise, in case the negative modifiers outnumber the
        positive ones too strong, the category is reduced by one level.
        """
        total = self.pos_mods - self.neg_mods
        threshold = 0.1 * (self.pos_mods + self.neg_mods)

        if total > threshold:
            mod = 1
        elif total < -threshold:
            mod = -1
        else:
            mod = 0

        self.category += mod
        self.reasons[f'mods: {self.pos_mods} vs {self.neg_mods}'] = mod

    def find_substring(self, start: str, end: str) -> str:
        startIdx = self.observed.find(start)
        if startIdx == -1:
            return ''

        startIdx += len(start)

        endIdx = self.observed.find(end, startIdx)
        if endIdx == -1:
            return ''

        if startIdx < endIdx:
            return self.observed[startIdx:endIdx]
        else:
            return ''

    def print(self) -> None:
        print()
        print(f'Rating: {self.category} stars')
        print()
        print(self.reasons)
        print()
