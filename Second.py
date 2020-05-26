import json
import sqlite3


def reader(file):
    try:
        with open(file, 'r') as f:
            dict_to_work_with = json.load(f)
            return dict_to_work_with
    except PermissionError:
        print('Permission error. Run script as administrator.')
    except Exception as ex:
        print(ex)
        print('Something goes wrong!')


def db(db_filename, json_dict):
    try:
        database = sqlite3.connect(db_filename)
        c = database.cursor()
        c.execute("CREATE TABLE Next_hop(next_hop text)")
        database.commit()
        next_hop = json_dict['route_table']['next hop'].keys()
        for net in next_hop:
            c.execute('''INSERT INTO Next_hop(next_hop) VALUES(?)''', (net,))
        database.commit()
        c.execute("CREATE TABLE Destination(next_hop text,Prf text, Metric text, Age integer, Interface text)")
        destination_data = []
        for hop in json_dict['route_table']['next hop']:
            # add next hops
            for key in json_dict['route_table']['next hop'][hop]:
                destination_data.append((hop, json_dict['route_table']['next hop'][hop][key]))
        for state in destination_data:
            c.execute('''INSERT INTO Destination(next_hop,Prf,Metric,Age,Interface) VALUES(?,?,?,?,?)''',
                      (state[0], state[1]['preference'], state[1]['metric'], state[1]['age'], state[1]['via']))
        database.commit()







        database.close()
        print('Done')
    except sqlite3.Error as error:
        print('db error : ', error)
        print('File already exist. u cant write ur data')


if __name__ == '__main__':
    try:
        input_data = input('Json file name : ')
        if input_data[-4:] == 'json':
            json_to_dict_data = reader(input_data)
            db(input('Database file name : '), json_to_dict_data)
        else:
            print('Not "json" format')
    except FileNotFoundError:
        print('File not found. try again.')
    except PermissionError:
        print('Permission error. Run script as administrator.')