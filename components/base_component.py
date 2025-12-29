from engine import Engine
from entity import Entity


class BaseComponent:
    entity: Entity  # Owning entity instance

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine
