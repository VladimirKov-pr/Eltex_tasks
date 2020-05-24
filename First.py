import json


def reader(inputfile):
    try:
        with open(inputfile, 'r') as outer:
            file_content = []
            output_data = []
            for line in outer:
                line.split()
                file_content.append(line)
            ref = [line.strip() for line in file_content]
            structure = [ele.split() for ele in ref]
            for i in range(len(structure)):
                for j in reversed(range(len(structure[i]))):
                    if structure[i][j] == '>' or structure[i][j] == 'via' or structure[i][j] == 'metric':
                        del structure[i][j]
            ind = 0
            for item in range(int(len(structure) / 2)):
                try:
                    if structure[ind + 2][0] == 'to':
                        output_data.append((structure[ind], structure[ind + 1] + structure[ind + 2]))
                        ind += 3
                    else:
                        output_data.append((structure[ind], (structure[ind + 1])))
                        ind += 2
                except IndexError:
                    output_data.append((structure[ind], structure[ind + 1]))
            print('Done')
            for d in output_data:
                print(d)
            return output_data
        # read data from logs and format it to elements of list
    except PermissionError:
        print('Permission error. Run script as administrator.')
    except FileNotFoundError:
        print('File not found. try again.')
    except Exception as ex:
        print(ex)
        print('Something goes wrong!')


def writer(outputfile, data):
    try:
        with open(outputfile, 'a') as inter:
            json.dump(data, inter, indent=4)
            print('Done')
        # write data to json file
    except FileNotFoundError:
        print('File not found. try again.')
    except PermissionError:
        print('Permission error. Run script as administrator.')
    except Exception as ex:
        print(ex)
        print('Something goes wrong!')


def convert_log_to_json_table(ref):
    # next hop loop
    destination_data_template = {}
    next_hop_template = dict()
    next_hop_struct = {'next hop': next_hop_template}
    route_table_template = {'route_table': next_hop_struct}
    for part in ref:
        ele = part[-1]
        for data in ele:
            i = 0
            if data == 'to':
                next_hop_template[ele[i + 1]] = ''
                i += 1

    list_of_keys_from_next_hop = next_hop_template.keys()
    list_of_destinations_from_keys_of_next_hop = []
    for part in ref:
        for participle in part:
            for data in participle:
                if data in list_of_keys_from_next_hop:
                    list_of_destinations_from_keys_of_next_hop.append([data, part[0][0]])
    for key in next_hop_template.keys():
        dict_of_destinations_from_next_hop = {}
        for parts in list_of_destinations_from_keys_of_next_hop:
            if parts[0] in key:
                dict_of_destinations_from_next_hop[parts[1]] = destination_data_template
                next_hop_template[parts[0]] = dict_of_destinations_from_next_hop
    for hopkey in next_hop_template.keys():
        for destkey in next_hop_template[hopkey]:
            for page in ref:
                dict_of_params_for_distinations = {'preference': page[0][1][-3:-1], 'metric': page[0][-1], 'age': (page[0][2] + ' ' + page[0][3][:-1]), 'via': page[1][2]}
                if page[0][0] == destkey:
                    next_hop_template[hopkey][destkey] = dict_of_params_for_distinations
                    print(next_hop_template)
                    break
    formated_data_output = route_table_template
    return formated_data_output


if __name__ == '__main__':
    open_file = input('File with logs: ')
    formated_data = reader(open_file)
    converted_data = convert_log_to_json_table(formated_data)
    writer(input('File to save as json data / File to add json data: '), converted_data)
    # ALERT!!! TERRIBLE CODE
