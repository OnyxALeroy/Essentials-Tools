import pandas as pd


def main():
    inputfile = "inputs/Trainer Battles.xlsx"
    data = pd.ExcelFile(inputfile)
    print(data)


if __name__ == "__main__":
    main()
