import csv, os
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.split(SCRIPT_PATH)[0]
STRAT_BULL_PATH = os.path.join(SCRIPT_DIR, "cache/bull_strat.csv")
STRAT_BEAR_PATH = os.path.join(SCRIPT_DIR, "cache/bear_strat.csv")
TRADE_HISTORY_PATH  = os.path.join(SCRIPT_DIR, "cache/trade_history.csv")
TRADE_HISTORY_HEADERS = ["time", "side", "strat", "exec_prirce", "quantity"]


def read_csv(file_path):
    data = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def write_csv(header, file_path, data):
    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for ele in data:
            writer.writerow(ele)


