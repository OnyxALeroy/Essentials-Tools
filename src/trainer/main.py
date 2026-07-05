import pandas as pd


def main():
    inputfile = "inputs/Trainer Battles.xlsx"
    xls = pd.ExcelFile(inputfile)

    for sheet in xls.sheet_names:
        if sheet != "BossBattlesRematches":
            continue

        df = pd.read_excel(xls, sheet, skiprows=range(1, 7))
        print(f"=== {sheet} ===")
        print()

        zones = []
        current_zone = None
        current_trainer = None

        for _, row in df.iterrows():
            infos = row["Infos"]

            if pd.isna(infos):
                if current_trainer is not None:
                    current_trainer["pokemon"].append(row.to_dict())

            elif infos == "Location:":
                current_zone = {"name": row["Pokemon"], "trainers": []}
                zones.append(current_zone)
                current_trainer = None

            elif current_zone is not None:
                current_trainer = {"name": infos, "pokemon": [row.to_dict()]}
                current_zone["trainers"].append(current_trainer)

        for zone in zones:
            print(f"  {zone['name']}")
            for trainer in zone["trainers"]:
                print(f"    {trainer['name']}")
                for mon in trainer["pokemon"]:
                    name = mon.get("Pokemon", "")
                    if pd.isna(name):
                        continue
                    lv = mon.get("Lv", "")
                    ivs = mon.get("IVs", "")
                    ability = mon.get("Ability", "")
                    nature = mon.get("Nature", "")
                    item = mon.get("Held Item", "")
                    moves = [mon.get(f"Move {i}", "") for i in range(1, 5)]
                    moves_str = " / ".join(m for m in moves if pd.notna(m))
                    item_str = f" @ {item}" if pd.notna(item) and item else ""
                    print(f"      - {name}{item_str}  Lv{lv}  {ivs}IVs  {ability}  {nature}  [{moves_str}]")
                print()
            print()


if __name__ == "__main__":
    main()
