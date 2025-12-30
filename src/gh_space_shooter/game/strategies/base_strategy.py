"""Base strategy interface for enemy clearing strategies."""

from abc import ABC, abstractmethod
from typing import Iterator

from ...github_client import ContributionData


class Action:
    """Represents a single action in the game."""

    def __init__(self, week: int, day: int, shoot: bool = False):
        """
        Initialize an action.

        Args:
            week: Week index (0-51)
            day: Day index (0-6, where 0=Sunday)
            shoot: Whether to shoot at this position
        """
        self.week = week
        self.day = day
        self.shoot = shoot

    def __repr__(self) -> str:
        action_type = "SHOOT" if self.shoot else "MOVE"
        return f"Action({action_type} week={self.week}, day={self.day})"


class BaseStrategy(ABC):
    """Abstract base class for enemy clearing strategies."""

    @abstractmethod
    def generate_actions(self, contribution_data: ContributionData) -> Iterator[Action]:
        """
        Generate sequence of actions for the ship to clear enemies.

        Args:
            contribution_data: The contribution graph data

        Yields:
            Action objects representing ship movements and shots
        """
        pass
