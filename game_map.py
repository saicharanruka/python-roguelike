from typing import Iterable
import numpy as np
from tcod.console import Console


from entity import Entity
import tile_types


class GameMap:
    def __init__(
        self, width: int, height: int, entities: Iterable[Entity] = ()
    ) -> None:
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map

        If a tile is in the "visible" array, then draw it with light colors
        If it isn't, but it's in the "explored" aray, then draw it with dark colors
        Otherwise, default is SHROUD
        """

        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,  # type: ignore
        )  # type: ignore

        for entity in self.entities:
            # Only print if in FOV
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, text=entity.char, fg=entity.color)
