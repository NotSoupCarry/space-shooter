"""Renderer for drawing game frames using Pillow."""

from PIL import Image, ImageDraw

from .game_state import GameState


class Renderer:
    """Renders game state as PIL Images."""

    # Cell size in pixels
    CELL_SIZE = 12
    CELL_SPACING = 2

    # Colors (RGB tuples)
    COLOR_BACKGROUND = (13, 17, 23)  # GitHub dark background
    COLOR_EMPTY = (22, 27, 34)  # Empty cell
    COLOR_SHIP = (88, 166, 255)  # Blue for ship
    COLOR_BULLET = (255, 223, 0)  # Yellow for bullets

    # Enemy colors based on health (GitHub green shades)
    COLOR_ENEMY = {
        1: (0, 109, 50),  # Level 1 - light green
        2: (38, 166, 65),  # Level 2 - medium green
        3: (57, 211, 83),  # Level 3 - bright green
        4: (87, 242, 135),  # Level 4 - very bright green
    }

    def __init__(self, game_state: GameState):
        """
        Initialize renderer.

        Args:
            game_state: The game state to render
        """
        self.game_state = game_state
        self.num_weeks, self.num_days = game_state.get_grid_dimensions()

        # Calculate image dimensions
        self.grid_width = self.num_weeks * (self.CELL_SIZE + self.CELL_SPACING)
        self.grid_height = self.num_days * (self.CELL_SIZE + self.CELL_SPACING)

        # Add padding for ship movement
        self.padding = 40
        self.width = self.grid_width + 2 * self.padding
        self.height = self.grid_height + 2 * self.padding

    def render_frame(self) -> Image.Image:
        """
        Render the current game state as an image.

        Returns:
            PIL Image of the current frame
        """
        # Create image with background color
        img = Image.new("RGB", (self.width, self.height), self.COLOR_BACKGROUND)
        draw = ImageDraw.Draw(img)

        # Draw grid and enemies
        self._draw_grid(draw)
        self._draw_enemies(draw)

        # Draw bullets
        self._draw_bullets(draw)

        # Draw ship
        self._draw_ship(draw)

        return img

    def _draw_grid(self, draw: ImageDraw.ImageDraw):
        """Draw the empty grid cells."""
        for week in range(self.num_weeks):
            for day in range(self.num_days):
                x, y = self._get_cell_position(week, day)
                draw.rectangle(
                    [x, y, x + self.CELL_SIZE, y + self.CELL_SIZE],
                    fill=self.COLOR_EMPTY,
                )

    def _draw_enemies(self, draw: ImageDraw.ImageDraw):
        """Draw all alive enemies."""
        for enemy in self.game_state.get_alive_enemies():
            x, y = self._get_cell_position(enemy.week, enemy.day)

            # Get color based on current health
            color = self.COLOR_ENEMY.get(enemy.health, self.COLOR_ENEMY[1])

            draw.rectangle(
                [x, y, x + self.CELL_SIZE, y + self.CELL_SIZE],
                fill=color,
            )

    def _draw_ship(self, draw: ImageDraw.ImageDraw):
        """Draw the ship."""
        ship = self.game_state.ship

        # Ship is drawn to the left of its current week position
        if ship.week >= 0:
            x, y = self._get_cell_position(ship.week, ship.day)
        else:
            # Ship off-screen to the left
            x = self.padding - 20
            y = self.padding + ship.day * (self.CELL_SIZE + self.CELL_SPACING)

        # Draw simple ship shape (triangle pointing right)
        ship_size = self.CELL_SIZE
        draw.polygon(
            [
                (x - ship_size, y),  # Left point (back)
                (x - ship_size, y + ship_size),  # Left bottom
                (x, y + ship_size // 2),  # Right point (front)
            ],
            fill=self.COLOR_SHIP,
        )

    def _draw_bullets(self, draw: ImageDraw.ImageDraw):
        """Draw all bullets."""
        for bullet in self.game_state.bullets:
            x, y = self._get_cell_position(bullet.week, bullet.day)

            # Draw bullet as small circle in center of cell
            center_x = x + self.CELL_SIZE // 2
            center_y = y + self.CELL_SIZE // 2
            radius = 3

            draw.ellipse(
                [
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                ],
                fill=self.COLOR_BULLET,
            )

    def _get_cell_position(self, week: int, day: int) -> tuple[int, int]:
        """
        Get the pixel position (x, y) of a cell.

        Args:
            week: Week index
            day: Day index

        Returns:
            Tuple of (x, y) pixel coordinates
        """
        x = self.padding + week * (self.CELL_SIZE + self.CELL_SPACING)
        y = self.padding + day * (self.CELL_SIZE + self.CELL_SPACING)
        return (x, y)
