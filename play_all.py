from collections import defaultdict
from joblib import Parallel, delayed
from pathlib import Path
import os

from games.hero_academy.heroac_action import HeroAcademyAction

def play_game(game_conf: str):
    os.system("python play_n_games.py " + game_conf)

if __name__ == "__main__":
    # conf_files = *map(str, Path("conf").rglob("*.json")),
    # Parallel(n_jobs=6)(delayed(play_game)(i) for i in conf_files)
    turn = [HeroAcademyAction(None, None, None)]
    print(turn)
    turn.clear()
    print(turn)