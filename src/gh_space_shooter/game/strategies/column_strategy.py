"""Column-by-column strategy: Ship moves week by week (left to right)."""

from typing import Iterator

from ...github_client import ContributionData
from .base_strategy import Action, BaseStrategy


class ColumnStrategy(BaseStrategy):
    """
    Ship moves column by column (week by week) from left to right.

    For each week, the ship shoots at all enemies (contributions > 0) in that column,
    hitting each enemy once per pass until all are destroyed.
    """

    def generate_actions(self, contribution_data: ContributionData) -> Iterator[Action]:
        """
        Generate actions moving week by week.

        The ship moves through each week (column), shooting at enemies
        until all enemies in that week are destroyed, then moves to the next week.

        Args:
            contribution_data: The contribution graph data

        Yields:
            Action objects representing ship movements and shots
        """
        weeks = contribution_data["weeks"]

        # Process each week (column)
        for week_idx in range(len(weeks)):
            week = weeks[week_idx]

            # Create a copy of enemy health for this week
            enemy_health = [day["level"] for day in week["days"]]

            # Keep shooting at enemies in this column until all are destroyed
            max_health = max(enemy_health) if enemy_health else 0

            # We need multiple passes to destroy high-health enemies
            for pass_num in range(max_health):
                # Shoot at each enemy position from top to bottom
                for day_idx in range(len(enemy_health)):
                    # Only shoot if enemy still has health
                    if enemy_health[day_idx] > 0:
                        yield Action(week=week_idx, day=day_idx, shoot=True)
                        enemy_health[day_idx] -= 1
                    else:
                        # Move through empty positions (no enemy or already destroyed)
                        yield Action(week=week_idx, day=day_idx, shoot=False)
