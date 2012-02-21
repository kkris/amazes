
from random_mouse import RandomMouse
from wall_follower import WallFollower
from tremaux import Tremaux, TremauxShortest
from flooding import Flooding

solving_algorithms = {
    'random_mouse': RandomMouse,
    'wall_follower': WallFollower,
    'tremaux': Tremaux,
    'tremaux_shortest': TremauxShortest,
    'flooding': Flooding,
}
