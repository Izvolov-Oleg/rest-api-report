from models import *
from datetime import datetime


def get_time_data(path: str) -> dict:
    """
    This func prepares data to get result.
    It takes a path(str), opens the file for reading and
    return data from file(for each racer) in dict like {"racer abbreviation" : data(datetime type)}
    """
    data = dict()
    with open(path, 'r') as f:
        for line in f.read().split('\n'):
            if line:  # if line isn't empty
                data[line[:3]] = datetime.strptime(
                    line[3:], '%Y-%m-%d_%H:%M:%S.%f')
    return data


def get_result(start: dict, end: dict) -> dict:
    """
    This func calculates the result.
    It takes 2 dicts (with the start data and the end data) and subtracts
    the difference between the end time and the start time for each racer.
    The func return dict like {"racer abbreviation" : result(timedelta type)}
    """
    result = dict()
    for key in end.keys():
        result[key] = end[key] - start[key]
    return result

def record_data(folder_path: str):
    """
    This func adds a race report in database.
    It takes the path to the data folder and
    adds data in databace using class Racer from models.
    """
    start_path = f'{folder_path}/start.log'
    end_path = f'{folder_path}/end.log'

    start_data = get_time_data(start_path)
    end_data = get_time_data(end_path)

    results = get_result(start_data, end_data)

    abbs = dict()
    with open("./abbreviations.txt", 'r') as f:
        for line in f.read().split('\n'):
            abbs[line[:3]] = line[4:].split('_')
    with db:
        for racer in results.keys():
            Racer.create(abbr_name=racer, name=abbs[racer][0], team=abbs[racer][1], result=results[racer])

if __name__ == '__main__':
    record_data('./data')

