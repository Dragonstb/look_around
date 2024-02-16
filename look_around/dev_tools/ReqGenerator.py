import numpy as np
import numpy.typing as npt

# company name
_letters = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
_entity_type = np.array(['SE', 'Holding', 'Ltd.'])

# company description

_cd_grammar = {
    '*start': [
        ['*S', '*CD', 'in', '*CL', '.', '*BS', '*BG', '*BT', '.'],
        ['*S', '*CD', 'in', '*CL', '.', '*BSa', '*BGa', '*BT', '.'],
        ['*S', '*CD', '*BG', '*CL', '.', '*BS', '*BG', '*BT', '.'],
        ['*S', '*CD', 'in', '*CL', '.', '*BSa', '*BGa', '*BT', '.'],
        ['*S', 'are', '*BG', '*CL']
    ],
    '*S': [['we'], ['our company'], ['{company_name}']],
    '*CD': [['are a', '*CA', '*C'], ['are a', '*C'], ['are', '*CH']],
    '*CL': [
        ['the field of', '*CF'],
        ['the', '*CF', 'sector'],
        ['the', '*CF', 'markets'],
    ],
    '*BS': [['our goal is'], ['with our products we']],
    '*BSa': [['with our solutions we']],
    '*BG': [
        ['*BR', '*BA', '*BI', 'for'],
        ['*BR', '*BI', 'for'],
        ['revolutionizing']
    ],
    '*BGa': [
        ['*BRa', '*BA', '*BI', 'for'],
        ['*BRa', '*BI', 'for'],
        ['revolutionizing']
    ],
    '*BT': [
        ['the use of {fields}'],
    ],
    '*CA': [['innovative'], ['family-led'], ['small'], ['large'], ['leading'], ['ambitious'], ['encouraged'], ['the leading']],
    '*C': [['company'], ['start up']],
    '*CH': [['the market leader'], ['the number one'], ['the largest'], ['one of the largest players']],
    '*BR': [['providing'], ['offering'], ['coming up with']],
    '*BRa': [['provide'], ['offer'], ['come up with']],
    '*BA': [['novel'], ['smart'], ['outstanding'], ['innovative']],
    '*BI': [['ideas'], ['solutions'], ['products'], ['services']],
    '*CF': [['energy'], ['logistics'], ['public health'], ['business intelligence'], ['software development'], ['B2B'], ['transport'], ['automotion']]
}

# yes, it is stupid for now. In the future, there will be lists for each field
_comp_fields = ['solar energy', 'wind energy', 'oil', 'coal', 'nuclear power', 'logistics', 'transport', 'screening', 'cancer prevention', 'data analysis',
                'process analysis', 'process mining', 'coding styles', 'cloud platforms', 'SaaS', 'traffic optimization', 'public transport', 'car sharing']

# experience discriminators
_min_quantifiers = np.array(['at least', 'minimum', 'not less than'])
_qualifiers = np.array(['first', 'profound', 'sound'])
_numbers = np.array(['one', 'two', 'three', 'four',
                     'five', 'six', 'seven', 'eight', 'nine'])
_xp = np.array(['experience in', 'knowledge of'])


class ReqGenerator:

    rand = np.random.default_rng()
    company_name: str = ''

    # _______________ company name _______________

    def getCompanyName(self) -> str:
        """
        Gets the company name. If the instance does not have such a name, one is generated.

        return:
        The company name stored in thsi instance.
        """
        if len(self.company_name) == 0:
            self.produceCompanyName()
        return self.company_name

    def produceCompanyName(self) -> None:
        """
        Generates a company name. Do not expect too much.

        return:
        An obviously very random company name.
        """
        rolls = self.rand.random(size=4)
        rollIdx = 0
        name = []

        # one or two individual names
        if rolls[rollIdx] < 0.8:
            numLetters = int(7 + 7 * rolls[rollIdx+1])
            name.append(
                ''.join(self.__pick_several_from_array(_letters, size=numLetters)))
        else:
            numLetters = int(4 + 3 * rolls[rollIdx+1])
            name.append(
                ''.join(self.__pick_several_from_array(_letters, size=numLetters)))
            numLetters = int(4 + 3 * rolls[rollIdx+2])
            name.append(
                ''.join(self.__pick_several_from_array(_letters, size=numLetters)))
        rollIdx = rollIdx + 3

        # entity type
        if rolls[rollIdx] < 0.8:
            name.append(self.__pick_from_array(_entity_type))

        self.company_name = ' '.join(name)

    # _______________ company description _______________

    def genCompanyDescription(self) -> str:
        """
        Generates a description of what the company works on.
        The result might be a bit funny, though :)

        returns:
        One or two sentences what the company does.
        """
        sentence = ['*start']
        while len(list(filter(lambda x: x[0] == '*', sentence))) > 0:
            # first element starting with *
            symbol = next(filter(lambda x: x[0] == '*', sentence))
            idx = sentence.index(symbol)

            options = _cd_grammar[symbol]
            insert = options[self.rand.integers(0, len(options))]
            sentence = sentence[:idx] + insert + sentence[idx+1:]

        numFields = self.rand.integers(1, 4)
        if numFields == 1:
            idx = self.rand.integers(0, len(_comp_fields))
            fields = _comp_fields[idx]
        elif numFields == 2:
            idx1 = self.rand.integers(0, len(_comp_fields))
            idx2 = self.rand.integers(0, len(_comp_fields))
            fields = _comp_fields[idx1] + ' and ' + _comp_fields[idx2]
        else:
            idx1 = self.rand.integers(0, len(_comp_fields))
            idx2 = self.rand.integers(0, len(_comp_fields))
            idx3 = self.rand.integers(0, len(_comp_fields))
            fields = _comp_fields[idx1] + ', ' + \
                _comp_fields[idx2] + ' and ' + _comp_fields[idx3]

        description = ' '.join(sentence)
        description = description.replace(' .', '.').capitalize()
        return description.format(company_name=self.getCompanyName(), fields=fields)

    # _______________ experience _______________

    def genExperienceLine(self, skill_targets: npt.NDArray[np.string_]) -> str:
        need_years = False
        sentence = []
        rolls = self.rand.random(size=2)
        counter = 0

        # quantifier or qualifier: how much experience
        if rolls[counter] < 0.25:
            val = self.__pick_from_array(_min_quantifiers)
            sentence.append(val)
            need_years = True
        elif rolls[counter] < 0.75:
            val = self.__pick_from_array(_qualifiers)
            sentence.append(val)
        else:
            need_years = True

        # number of yers: only when the stentence starts with a minimum quantifier
        if need_years:
            val = self.__pick_from_array(_numbers)
            sentence.append(val)
            if val != 'one':
                sentence.append('years of')
            else:
                sentence.append('year of')

        # experience or knowledge? A number of years enforces the experience
        counter = counter + 1
        if need_years or rolls[counter] < 0.15:
            sentence.append('experience in')
        else:
            val = self.__pick_from_array(_xp)
            sentence.append(val)

        # skill targets
        picks = self.rand.integers(
            1, np.min([3, skill_targets.shape[0]]), endpoint=True)
        idx = np.random.choice(
            skill_targets.shape[0], size=picks, replace=False)
        targets = skill_targets[idx]
        if targets.shape[0] > 2:
            lastTarget = 'and ' + targets[-1]
            targets[-1] = lastTarget
            skills = ', '.join(targets)
        elif targets.shape[0] == 2:
            skills = ' and '.join(targets)
        else:
            skills = targets[0]
        sentence.append(skills)

        # concatenate and return
        return ' '.join(sentence)

    # _______________ utilities _______________

    def __pick_from_array(self, arr: npt.NDArray):
        idx = self.rand.integers(0, arr.shape[0])
        return arr[idx]

    def __pick_several_from_array(self, arr: npt.NDArray, size: int = 1, replace: bool = True) -> npt.NDArray:
        """
        Picks several randomly taken elements from the array.

        arr:
        Array the sample is taken from.

        size (default 1):
        Sample size.

        replace (default True):
        Should an extracted sample be replaced (i.e. it can be drawn more than once)?

        return:
        Array with randomly chosen samples.
        """
        idx = np.random.choice(arr.shape[0], size=size, replace=replace)
        return arr[idx]

    def _test_experience(self):
        arr = np.array(['RPG', 'Video Games', 'Console Games',
                       'Board Games', 'Card Games', 'Computer Games'])
        return self.genExperienceLine(arr)

    def _test_company_name(self):
        return self.getCompanyName()

    def _test_company_desc(self):
        return self.genCompanyDescription()
