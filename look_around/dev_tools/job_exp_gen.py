import numpy as np
import numpy.typing as npt
from dev_tools import utils

# experience discriminators
_min_quantifiers = np.array(['at least', 'minimum', 'not less than'])
_qualifiers = np.array(['first', 'profound', 'sound'])
_numbers = np.array(['one', 'one', 'one', 'one', 'two', 'two', 'two', 'three', 'three', 'three', 'four', 'four', 'five',
                     'five', 'six', 'six', 'seven', 'eight', 'nine'])
_xp = np.array(['experience in', 'knowledge of'])


class JobExpGen:

    rand: np.random.Generator
    """A random number generator"""

    def __init__(self) -> None:
        self.rand = np.random.default_rng()

    def gen_experience_line(self, skill_targets: npt.NDArray[np.str_]) -> str:
        """
        Generates a line describing a job requirement or an expected experience in
        or knowledge about a certain topic/entity.

        skill_targets:
        The requested skills are picked from this list.

        returns:
        A line that demands some knowledge.
        """
        need_years = False
        sentence = []
        rolls = self.rand.random(size=2)
        counter = 0

        # quantifier or qualifier: how much experience
        if rolls[counter] < 0.25:
            val = utils.pick_from_array(_min_quantifiers)
            sentence.append(val)
            need_years = True
        elif rolls[counter] < 0.75:
            val = utils.pick_from_array(_qualifiers)
            sentence.append(val)
        else:
            need_years = True

        # number of yers: only when the stentence starts with a minimum quantifier
        if need_years:
            val = utils.pick_from_array(_numbers)
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
            val = utils.pick_from_array(_xp)
            sentence.append(val)

        # skill targets
        picks = self.rand.integers(
            1, np.min([3, skill_targets.shape[0]]), endpoint=True)
        idx = np.random.choice(
            skill_targets.shape[0], size=picks, replace=False)
        targets = skill_targets[idx]
        if targets.shape[0] > 2:
            skills = targets[0]+', '+targets[1]+', and '+targets[2]
        elif targets.shape[0] == 2:
            skills = ' and '.join(targets)
        else:
            skills = targets[0]
        sentence.append(skills)

        # concatenate and return
        return ' '.join(sentence)

    # _______________ utilities _______________

    def _test_experience(self):
        arr = np.array(['RPG', 'Video Games', 'Console Games',
                       'Board Games', 'Card Games', 'Computer Games'])
        return self.gen_experience_line(arr)
