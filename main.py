import tcod

from engine import Engine
from entity import Entity
from proc_gen import generate_dungeon
from input_handlers import EventHandler


def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(
        x=int(screen_width / 2),
        y=int(screen_height / 2),
        char="@",
        color=(255, 255, 255),
    )
    # npc = Entity(
    #     x=int(screen_width / 2 - 5),
    #     y=int(screen_height / 2 - 5),
    #     char="@",
    #     color=(255, 255, 0),
    # )
    # entities = {player, npc}

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
    )

    engine = Engine(event_handler=event_handler, player=player, game_map=game_map)

    # screen
    with tcod.context.new(
        width=screen_width,
        height=screen_height,
        tileset=tileset,
        title="Python Rougelike",
        vsync=True,
    ) as context:
        # console
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
