from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

# from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(
        self,
        event_handler: EventHandler,
        player: Entity,
        game_map: GameMap,
    ) -> None:
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_events(self, events: Iterable[Any]):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.update_fov()

    def update_fov(self) -> None:
        """Compute the visible area based of player's FOV"""

        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )
        # If a tile is "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        # for entity in self.entities:
        #     # console.print(entity.x, entity.y, text=entity.char, fg=entity.color)
        #     # Only prints entities in FOV
        #     if self.game_map.visible[entity.x, entity.y]:
        #         console.print(entity.x, entity.y, text=entity.char, fg=entity.color)

        context.present(console)
        console.clear()
