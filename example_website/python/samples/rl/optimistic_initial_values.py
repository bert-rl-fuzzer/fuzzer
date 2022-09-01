import logging

import numpy as np

from samples.rl.bandit import (
    Agent,
    Bandit,
)


logger = logging.getLogger(__name__)


class OptimisticInitialValuesAgent(Agent):
    def __init__(self, max_reward: float):
        super().__init__()
        self.max_reward = max_reward

    def _get_current_best_bandit(self) -> Bandit:
        estimates = []
        for bandit in self.bandits:
            bandit_record = self.rewards_log[bandit]
            if not bandit_record['actions']:
                estimates.append(self.max_reward)
            else:
                estimates.append(
                    (self.max_reward + bandit_record['reward']) / (1 + bandit_record['actions']),
                )

        return self.bandits[np.argmax(estimates)]

    def take_action(self):
        current_bandit = self._get_current_best_bandit()
        reward = current_bandit.pull()
        self.rewards_log.record_action(current_bandit, reward)
        return reward

    def __repr__(self):
        return 'OptimisticInitialValuesAgent(max_reward={})'.format(self.max_reward)
