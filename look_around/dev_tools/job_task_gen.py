import numpy as np

_grammar = {
    '*start': [
        ['*setup', '*obj_and_empty', '*projects', '*target'],
        ['*setup', '*obj_and_empty', '*databases', '*target'],
        ['*setup', '*obj', '*programs', '*target'],
        ['*communicate', '*obj', '*groups', '*on']
    ],
    '*obj': [
        ['our'],
        ['the']
    ],
    '*obj_and_empty': [
        [''],
        ['our'],
        ['the']
    ],
    '*link': [
        ['together with'],
        ['for']
    ],
    '*target': [
        ['*link', '*obj', '*groups'],
        ['']
    ],
    '*on': [
        [''],
        ['on', '*obj_and_empty', '*work'],
        ['on', '*obj_and_empty', '*work', 'when', '*settingup', 'the', '*work']
    ],
    '*work': [
        ['*databases'], ['*programs'], ['*projects']
    ],

    '*setup': [['{operate}'], ['{implement}'], ['*implement', 'and', '*operate']],
    '*settingup': [['{operating}'], ['{implementing}'], ['*implementing', 'and', '*operating']],
    '*operate': [['run'], ['maintain'], ['operate']],
    '*operating': [['running'], ['maintaining'], ['operating']],
    '*implement': [['implement'], ['develop'], ['design'], ['set up'], ['define']],
    '*implementing': [['implementing'], ['developing'], ['designing'], ['seting up'], ['defining']],

    '*communicate': [['communicate to'], ['be the first contact for'], ['support'], ['work with']],

    '*databases': [['databases'], ['data warehouses'], ['data lakes'], ['ETL pipe lines']],
    '*programs': [['SaaS platform'], ['software tools'],
                  ['algorithms'], ['machine learning tools']],
    '*projects': [['client projects'], ['customer projects']],
    '*groups': [['customers'], ['clients'], ['internal business teams'], ['company']]
}

_operate = ['run', 'maintain', 'operate']
_operating = ['running', 'maintaining', 'operating']
_implement = ['implement', 'develop', 'design', 'set up', 'define']
_implementing = ['implementing', 'developing',
                 'designing', 'seting up', 'defining']


class JobTaskGen:

    rand = np.random.default_rng()

    def __init__(self) -> None:
        pass

    def gen_job_task(self) -> str:
        """
        Generates a task you have to to in this job.

        return:
        A string that describes a labour you have to in the job.
        """
        sentence = ['*start']
        while len(list(filter(lambda x: len(x) > 0 and x[0] == '*', sentence))) > 0:
            # first element starting with *
            symbol = next(filter(lambda x: len(
                x) > 0 and x[0] == '*', sentence))
            idx = sentence.index(symbol)

            options = _grammar[symbol]
            insert = options[self.rand.integers(0, len(options))]
            sentence = sentence[:idx] + insert + sentence[idx+1:]

        rolls = self.rand.random(size=4)

        if rolls[0] < 0.75:
            idx = self.rand.integers(0, len(_operate))
            operate = _operate[idx]
        else:
            idx1 = self.rand.integers(0, len(_operate))
            idx2 = self.rand.integers(0, len(_operate))
            operate = _operate[idx1] + ' and ' + _operate[idx2]

        if rolls[1] < 0.75:
            idx = self.rand.integers(0, len(_operating))
            operating = _operating[idx]
        else:
            idx1 = self.rand.integers(0, len(_operating))
            idx2 = self.rand.integers(0, len(_operating))
            operating = _operating[idx1] + ' and ' + _operating[idx2]

        if rolls[2] < 0.75:
            idx = self.rand.integers(0, len(_implement))
            implement = _implement[idx]
        else:
            idx1 = self.rand.integers(0, len(_implement))
            idx2 = self.rand.integers(0, len(_implement))
            implement = _implement[idx1] + ' and ' + _implement[idx2]

        if rolls[3] < 0.75:
            idx = self.rand.integers(0, len(_implementing))
            implementing = _implementing[idx]
        else:
            idx1 = self.rand.integers(0, len(_implementing))
            idx2 = self.rand.integers(0, len(_implementing))
            implementing = _implementing[idx1] + ' and ' + _implementing[idx2]

        description = ' '.join(sentence)
        description = description.replace(' .', '.').replace('  ', ' ').strip()
        return description.format(operate=operate, operating=operating, implement=implement, implementing=implementing)
