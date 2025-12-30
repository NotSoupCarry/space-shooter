"""Game state management for tracking enemies, ship, and bullets."""

from typing import List, Tuple

from ..github_client import ContributionData


class Enemy:
    """Represents an enemy at a specific position."""

    def __init__(self, week: int, day: int, health: int):
        """
        Initialize an enemy.

        Args:
            week: Week position (0-51)
            day: Day position (0-6)
            health: Initial health/lives (1-4)
        """
        self.week = week
        self.day = day
        self.health = health
        self.max_health = health

    def take_damage(self) -> bool:
        """
        Enemy takes 1 damage.

        Returns:
            True if enemy is destroyed (health <= 0), False otherwise
        """
        self.health -= 1
        return self.health <= 0

    def is_alive(self) -> bool:
        """Check if enemy is still alive."""
        return self.health > 0


class Bullet:
    """Represents a bullet fired by the ship."""

    def __init__(self, week: int, day: int):
        """
        Initialize a bullet.

        Args:
            week: Current week position
            day: Current day position (target)
        """
        self.week = week
        self.day = day


class Ship:
    """Represents the player's ship."""

    def __init__(self):
        """Initialize the ship at starting position."""
        self.week = -1  # Start off-screen to the left
        self.day = 3  # Middle of the screen (roughly)

    def move_to(self, week: int, day: int):
        """
        Move ship to a new position.

        Args:
            week: Target week
            day: Target day
        """
        self.week = week
        self.day = day


class GameState:
    """Manages the current state of the game."""

    def __init__(self, contribution_data: ContributionData):
        """
        Initialize game state from contribution data.

        Args:
            contribution_data: The GitHub contribution data
        """
        self.contribution_data = contribution_data
        self.ship = Ship()
        self.enemies: List[Enemy] = []
        self.bullets: List[Bullet] = []

        # Initialize enemies from contribution data
        self._initialize_enemies()

    def _initialize_enemies(self):
        """Create enemies based on contribution levels."""
        weeks = self.contribution_data["weeks"]
        for week_idx, week in enumerate(weeks):
            for day_idx, day in enumerate(week["days"]):
                level = day["level"]
                if level > 0:  # Only create enemy if there are contributions
                    enemy = Enemy(week=week_idx, day=day_idx, health=level)
                    self.enemies.append(enemy)

    def get_enemy_at(self, week: int, day: int) -> Enemy | None:
        """
        Get enemy at a specific position.

        Args:
            week: Week position
            day: Day position

        Returns:
            Enemy if one exists at that position, None otherwise
        """
        for enemy in self.enemies:
            if enemy.week == week and enemy.day == day and enemy.is_alive():
                return enemy
        return None

    def shoot(self, week: int, day: int):
        """
        Ship shoots a bullet at target position.

        Args:
            week: Target week
            day: Target day
        """
        # Create bullet
        bullet = Bullet(week=week, day=day)
        self.bullets.append(bullet)

        # Check if bullet hits an enemy
        enemy = self.get_enemy_at(week, day)
        if enemy:
            if enemy.take_damage():
                # Enemy destroyed, will be filtered out
                pass

    def clear_bullets(self):
        """Clear all bullets from the screen."""
        self.bullets.clear()

    def get_alive_enemies(self) -> List[Enemy]:
        """Get list of all alive enemies."""
        return [enemy for enemy in self.enemies if enemy.is_alive()]

    def is_complete(self) -> bool:
        """Check if game is complete (all enemies destroyed)."""
        return len(self.get_alive_enemies()) == 0

    def get_grid_dimensions(self) -> Tuple[int, int]:
        """
        Get the dimensions of the game grid.

        Returns:
            Tuple of (num_weeks, num_days)
        """
        return (len(self.contribution_data["weeks"]), 7)
