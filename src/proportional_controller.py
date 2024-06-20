import numpy as np


class ProportionalController:
    def __init__(self):
        pass

    def update(self, target_rate, actual_rate, dt):
        """
        Choose a to enter a bid based on the proportion of budget spent
        """
        p = (target_rate - actual_rate) / target_rate
        #ensure p is between 0 and 1
        p = max(0, min(1, p))
        return np.random.choice([0, 1], p=[1-p, p])