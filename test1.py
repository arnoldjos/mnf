#! /usr/bin/python3

import argparse
import subprocess
import pandas as pd

 
parser = argparse.ArgumentParser(description='Input country')
parser.add_argument('-j', '--jitter', type=float, default='50',
                    help='Maximum Jitter Value')
parser.add_argument('-l', '--latency', type=float, default='50',
                    help='Maximum Latency value')
args = parser.parse_args()

max_jitter = vars(args)['jitter']
max_latency = vars(args)['latency']

def get_chrony_data():
    """
    This function runs the chrony command and maps it properly then return
    a list of dictionaries based on the results from the command.
    """

    cmd = ['chronyc', '-n', 'sources']
    # Run command to get chronyc data
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        counter = 0
        data = []
        column_names = []
        for line in proc.stdout.readlines():
            line_str = line.decode()           
            if counter == 1:
                cols = line_str.split()
                # Loop through column names to format data properly
                for idx, val in enumerate(cols):
                    col_name = val
                    if idx == 1 or idx ==7:
                        # Concatenate Name/IP address because split by string
                        col_name = f'{cols[idx]} {cols[idx + 1]}'
                    elif idx > 7 or idx == 2:
                        continue
                    column_names.append(col_name)
            elif counter >= 3:
                raw_rows = line_str.split()
                rows = [] 
                # Loop through the raw rows to format data properly
                for idx, val in enumerate(raw_rows):
                    row = val
                    if idx == 6:
                        # Concatentate data for last sample because split by string
                        row = ' '.join(raw_rows[idx: len(raw_rows)])
                    elif idx > 6:
                        break
                    rows.append(row)
                data.append(rows)
            counter += 1
    df = pd.DataFrame(data, columns=column_names)
    return df.to_dict('records')

def main():
    chrony = get_chrony_data()

    for c in chrony:
        source = c.get('MS') + ' ' + c.get('Name/IP address')
        latency = float(int(c.get('Last sample', '').split()[-1].replace('ms', '').replace('ns', '')))
        jitter = float(int(c.get('Reach')))

        # Check if jitter and latency depending on max values passed
        if jitter > max_jitter or latency > max_latency:
            if jitter > jitter and latency > latency:
                print(f'JITTER AND LATENCY CRITICAL source={source} | latency = {latency},jitter = {jitter} | ', end='')
            elif jitter > max_jitter:
                print(f'JITTER CRITICAL source={source} | jitter = {latency},latency={jitter} | ', end='')
            else:
                print(f'LATENCY CRITICAL source={source} | latency = {latency},jitter = {jitter} | ', end='')
            print(f'maxlatency = {max_latency},maxjitter = {max_jitter}')
        else:
            print(f'SOURCE OK - source = {source} | latency = {latency}, jitter = {jitter}')


if __name__ == '__main__':
    main()

