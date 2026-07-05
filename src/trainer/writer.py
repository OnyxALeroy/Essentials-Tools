import re

from .models import Trainer


def _to_key(s: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def _nature_key(s: str) -> str:
    return s.split(" (")[0].upper()


def write_trainers(trainers: list[Trainer], path: str) -> None:
    with open(path, "w") as f:
        f.write("# See the documentation on the wiki to learn how to edit this file.\n")
        for t in trainers:
            f.write("#-------------------------------\n")
            f.write(f"[{t.trainer_class},{t.trainer_name}]\n")
            for mon in t.team:
                if not mon.name:
                    continue
                lv = int(mon.level) if mon.level is not None else 0
                f.write(f"Pokemon = {_to_key(mon.name)},{lv}\n")
                if mon.ivs is not None:
                    iv = int(mon.ivs)
                    f.write(f"    IV = {iv},{iv},{iv},{iv},{iv},{iv}\n")
                if mon.held_item:
                    f.write(f"    Item = {_to_key(mon.held_item)}\n")
                if mon.ability:
                    f.write(f"    Ability = {_to_key(mon.ability)}\n")
                if mon.nature:
                    f.write(f"    Nature = {_nature_key(mon.nature)}\n")
                if mon.moves:
                    f.write(f"    Moves = {','.join(_to_key(m) for m in mon.moves)}\n")
