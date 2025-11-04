"""
Ship Catalogues by Faction
"""

from game.ships.federation import (
    FEDERATION_CATALOGUE,
    get_federation_ship,
    get_federation_ships_by_rank,
    get_all_federation_ships,
    get_federation_ships_at_rank,
    create_starting_ship
)

__all__ = [
    'FEDERATION_CATALOGUE',
    'get_federation_ship',
    'get_federation_ships_by_rank',
    'get_all_federation_ships',
    'get_federation_ships_at_rank',
    'create_starting_ship'
]
