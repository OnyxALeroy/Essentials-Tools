import pandas as pd

from .models import Pokemon, Trainer


def _val(v):
    return None if pd.isna(v) else v


def parse_sheet(sheet: str) -> list[Trainer]:
    xls = pd.ExcelFile("inputs/Trainer Battles.xlsx")
    df = pd.read_excel(xls, sheet, skiprows=range(1, 7))

    trainers = []
    current_location = None

    for _, row in df.iterrows():
        infos = _val(row["Infos"])

        if infos is None:
            if trainers and trainers[-1].team:
                team = trainers[-1].team
                team.append(_row_to_pokemon(row))

        elif infos == "Location:":
            current_location = _val(row["Pokemon"])

        else:
            tc, tn = infos.rsplit(" ", 1) if " " in infos else (infos, "")
            trainer = Trainer(trainer_class=tc, trainer_name=tn, location=current_location)
            trainer.team.append(_row_to_pokemon(row))
            trainers.append(trainer)

    return trainers


def _row_to_pokemon(row) -> Pokemon:
    name = _val(row["Pokemon"])
    return Pokemon(
        name=name,
        name_fr=_val(row.get("Pokemon (FR)")),
        level=_val(row.get("Lv")),
        ivs=_val(row.get("IVs")),
        ability=_val(row.get("Ability")),
        nature=_val(row.get("Nature")),
        held_item=_val(row.get("Held Item")),
        moves=[_val(row.get(f"Move {i}")) for i in range(1, 5) if _val(row.get(f"Move {i}"))],
    )


def show(trainers: list[Trainer]) -> None:
    seen = set()
    for t in trainers:
        loc = t.location
        if loc in seen:
            continue
        seen.add(loc)
        print(f"  {loc}")
        for t in trainers:
            if t.location != loc:
                continue
            print(f"    {t.trainer_class} {t.trainer_name}")
            for mon in t.team:
                if not mon.name:
                    continue
                item = f" @ {mon.held_item}" if mon.held_item else ""
                moves = " / ".join(m for m in mon.moves if m)
                print(f"      - {mon.name}{item}  Lv{mon.level}  {mon.ivs}IVs  {mon.ability}  {mon.nature}  [{moves}]")
            print()
        print()


def main():
    trainers = parse_sheet("BossBattlesRematches")
    print(f"=== BossBattlesRematches ({len(trainers)} trainers) ===")
    print()
    show(trainers)


if __name__ == "__main__":
    main()
