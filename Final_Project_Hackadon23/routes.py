#working for Gene


import csv
from datetime import datetime

schedule = []

with open('sample.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for line_count, row in enumerate(csv_reader):
        if line_count == 0:
            pass
        elif row == []:
            break
        else:
            starting = row[0]
            destination = row[1]
            busnumber = row[2]
            time = row[3]

            schedule.append([starting, destination, busnumber, time])


def calculate_time(starting_point, end_point, current_time):
    difference = None
    target = None

    for item in schedule:
        departure_time = item[3]
        t1 = datetime.strptime(current_time.strip(), '%H:%M')
        t2 = datetime.strptime(departure_time.strip(), '%H:%M')

        if (item[0].lower() == starting_point.lower()) and (item[1].strip().lower() == end_point.strip().lower()) and (t2 > t1):
            delta = t2 - t1
            current_difference = delta.total_seconds()

            if difference is None:
               difference = current_difference
               target = item

            else:
                if current_difference < difference:
                    difference = current_difference
                    target = item

    if target:
        return f'Take bus number{target[2]} departing at{target[3]}.'
    else:
        return "No possible routes"



