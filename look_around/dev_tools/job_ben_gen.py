import numpy as np
from typing import List
import numpy.typing as npt
import utils


_support = ['Free', 'Subsidized']


class JobBenGen:
    """
    Provides lists of benefits for a job.
    """

    rand: np.random.Generator

    def __init__(self) -> None:
        self.rand = np.random.default_rng()

    def gen_benefits(self, min: int, max: int) -> npt.NDArray:
        numAvailableBenefits = 13
        rolls = self.rand.random(size=numAvailableBenefits)
        allBens = []
        # pension
        allBens.append('Pension')
        # number of holidays
        numHolidays = self.rand.integers(25, 36)
        allBens.append(f'{numHolidays} days off per year')
        # car
        if (rolls[0] < 0.5):
            allBens.append('Company car')
        else:
            support = _support[self.rand.integers(0, 2)]
            allBens.append(f'{support} company car')
        # bike
        if (rolls[1] < 0.5):
            allBens.append('Company bike')
        else:
            support = _support[self.rand.integers(0, 2)]
            allBens.append(f'{support} company bike')
        # health insurance
        if (rolls[2] < 0.5):
            allBens.append('Health insurance')
        else:
            support = _support[self.rand.integers(0, 2)]
            allBens.append(f'{support} health insurance')
        # working hours
        numWorkingHours = self.rand.integers(30, 46)
        allBens.append(f'{numWorkingHours} working hours per week')
        # working days
        numWorkingDays = self.rand.integers(3, 6)
        allBens.append(f'{numWorkingDays} working days per week')
        # membership in a club
        allBens.append('Subsidized membership in a club')
        # bonus salary
        allBens.append('Bonus payment depending on your performance')
        # fruit basket
        allBens.append('Fruit basket')
        # cookie basket
        allBens.append('Cookie basket')
        # canteen
        if (rolls[3] < 0.5):
            allBens.append('Access to the canteen of the company')
        else:
            support = _support[self.rand.integers(0, 2)]
            allBens.append(f'{support} food in the canteen of the company')
        # mobile working
        if (rolls[4] < 0.5):
            allBens.append('Work from home whenever you want to do so')
        else:
            homeOfficeDays = self.rand.integers(2, 5)
            allBens.append(
                f'You can work from home on up to {homeOfficeDays} days per week')

        arr = np.array(allBens)
        numBenefits = self.rand.integers(
            min, 1+np.min([numAvailableBenefits, max]))
        return utils.pick_several_from_array(arr, size=numBenefits, replace=False)

    def _test_gen(self, count: int = 4):
        arr = self.gen_benefits(count, count)
        [print(f'{idx}\t'+arr[idx]) for idx in range(count)]
