class BudgetOnlyController:
    def __init__(self):
        pass

    def update(self, target_rate, actual_rate, dt):
        """
        If budget is not met, enter a bid.
        """

        return int(actual_rate < target_rate)