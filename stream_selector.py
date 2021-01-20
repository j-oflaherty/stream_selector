import json
import pprint

import sys  # get the arguments from cmd
import os
from time import sleep


def get_streams(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        contents = f.readlines()
    catalog = str()
    for line in contents:
        catalog += line
    return json.loads(catalog)['streams']


def stream_picker(streams: list) -> list:
    print('This are the streams available. If the stream your are looking for is missing run a discovery\n')
    for i in range(0, len(streams)):
        print(str(i)+'-', streams[i]['stream'])
    print('\nPlease enter the number(s) of the stream(s) you want to select separated by a coma (,)')
    user_input = set(input().strip(' ').split(','))
    selected_streams = list(user_input)
    selected_streams.sort()
    return selected_streams


def stream_treatment(stream: dict):

    # Stream selection
    i = 0
    while (i < len(stream['metadata'])) and (len(stream['metadata'][i]['breadcrumb']) != 0):
        i += 1
    stream['metadata'][i]['metadata']['selected'] = True

    # -----------------------------

    res = input('\nDo you want to modify the schema of the stream {}?[Y/N]: '.format(stream['stream']))
    while not(res.lower() in ['y', 'n']):
        print('Sorry, that isn\'t a valid input')
        res = input('Do you want to modify the schema of the stream?[Y/N]: ')
        print('')

    if res.lower() == 'y':
        schema_treatment(stream)


def schema_treatment(stream):
    confirm = False
    while not confirm:
        print('The properties found for this stream are the following:')
        i = 0
        key_numbers = dict()
        for key in stream['schema']['properties']:
            print(str(i) + '-', key)
            key_numbers[i] = key
            i += 1

        nums = set(input('Enter the numbers of the properties yo want to DROP from the stream separated by a coma (,'
                         '): \n').strip(' ').split(','))
        if len(nums) > 0 and not('' in nums):
            print('\nYou\'ve selected the following properties to be deleted:')
            nums = list(nums)
            for i in range(0, len(nums)):
                nums[i] = int(nums[i])
                print(key_numbers[nums[i]])
        else:
            print('\nYou haven\'t selected any properties')

        res = input('Do you want to confirm your selection[Y/N]: ')
        while not(res.lower() in ['y', 'n']):
            res = input('Do you want to confirm your selection[Y/N]: ')
        confirm = res.lower() == 'y'

    if len(nums) > 0 and not('' in nums):
        nums.sort(reverse=True)  # Borramos del último al primero para que no se modifiquen los indices
        for i in nums:
            stream['schema']['properties'].pop(key_numbers[i])
            j = 0
            while j < len(stream['metadata']):
                try:
                    if stream['metadata'][j]['breadcrumb'][1] == key_numbers[i]:
                        break
                    j += 1
                except IndexError:
                    j += 1
            stream['metadata'].pop(j)
        print('The selected properties where deleted\n')
    else:
        print('No changes where made to {}\n'.format(stream['stream']))


def main(file_path):
    try:
        streams = get_streams(file_path)
    except json.decoder.JSONDecodeError:
        print('An error occurred when trying to decode the file. Please check that the file contains a valid json '
              'structure')
        return None  # end execution on error

    confirm = False
    while not confirm:
        selected_streams = stream_picker(streams)
        print('You\'ve selected the following streams:')
        for k in selected_streams:
            print(streams[int(k)]['stream'])
        res = input('\nDo you want to confirm your selection?[Y/N]: ')
        while not(res.lower() in ['y', 'n']):
            res = input('\nDo you want to confirm your selection?[Y/N]:')
        confirm = (res.lower() == 'y')

    for k in selected_streams:
        stream_treatment(streams[int(k)])

    catalog = {"streams": streams}
    with open(file_path, 'w') as f:
        f.write(json.dumps(catalog, indent=2, sort_keys=True))


def file_selector(files: list):
    print("Here are the files available for treatment: ")
    sleep(1)
    i = 0
    for file in files:
        print(str(i) + '-', file)
        i += 1
    print('Please enter the number corresponding to the file you want to treat. If the file(s) you '
          'want to treat don\'t appear please check that the folder path provided is correct')
    index = int(input('File number: '))
    return files[index]


def welcome():
    print(r'''
███████╗████████╗██████╗ ███████╗ █████╗ ███╗   ███╗    ███████╗███████╗██╗     ███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗████╗ ████║    ██╔════╝██╔════╝██║     ██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
███████╗   ██║   ██████╔╝█████╗  ███████║██╔████╔██║    ███████╗█████╗  ██║     █████╗  ██║        ██║   ██║   ██║██████╔╝
╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║    ╚════██║██╔══╝  ██║     ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
███████║   ██║   ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║    ███████║███████╗███████╗███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚══════╝╚══════╝╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
''')
    sleep(1)
    print('Welcome to the stream selector. Follow the instructions as they appear on the screen')


if __name__ == '__main__':
    welcome()
    sleep(2)
    folder_path = sys.argv
    if len(folder_path) == 1:
        print('You forgot to specify the folder where the streams are.')
        print('Remember to execute the script with the following syntax:')
        print('     ~$ python folder_path')
        print('If you are in the currently in the folder folder_path="."')
    else:
        folder_path = folder_path[1]
        if not os.path.exists(folder_path):
            print('There isn\'t a folder with the path  {}/{}'.format(os.path.abspath(os.curdir), folder_path) )
            print('This script is beign executed from ' + os.path.abspath(os.curdir))

        else:
            available_files = os.listdir(folder_path)
            treatment: bool = True
            while treatment:
                file_path = folder_path + '/' + file_selector(available_files)
                print(file_path)
                print('\nStarting treatment on {}\n'.format(file_path[len(folder_path):]))
                sleep(2)
                main(file_path)
                sleep(2)
                treatment = input('Do you want to treat another file?[y/N]: ').lower() == 'y'
                print('\n\n')

