from __future__ import annotations
from typing import TYPE_CHECKING
import color

if TYPE_CHECKING:
    from tcod import console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, gamemap: GameMap) -> str:
    if not gamemap.in_bounds(x, y) or not gamemap.visible[x, y]:
        return ""
    names = ", ".join(
        entity.name for entity in gamemap.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(
    console: console.Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value / maximum_value * total_width))

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )
    console.print(
        x=1, y=45, text=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )


def render_names_at_mouse_location(
    console: console.Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x,  # type: ignore
        y=mouse_y,  # type: ignore
        gamemap=engine.game_map,
    )
    # print(names_at_mouse_location)
    console.print(x=x, y=y, text=names_at_mouse_location)
