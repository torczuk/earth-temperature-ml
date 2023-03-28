from pathlib import Path
import itertools
import re
import csv
import os

def berkleyearth_dataset_header(h1, h2):
    #  Converts below format into headers
    #  %               Monthly    Annual     Five-year  Ten-year   Twenty-year
    #  % Year, Month,  Anomaly,   Anomaly,   Anomaly,   Anomaly,   Anomaly
    #  year, month, monthly_anomaly ...

    headers = []
    h1_words = re.findall(r'[\w-]+', h1)
    h2_words = re.findall(r'[\w-]+', h2)
    h1_words.reverse()
    h2_words.reverse()
    merged = list(itertools.zip_longest(h1_words, h2_words))
    merged.reverse()
    for h1_word, h2_word in merged:
        header = '_'.join(filter(None, [h1_word, h2_word]))
        formatted = header.lower().replace('-','_')
        headers.append(formatted)
    return headers;

def berkleyearth_dataset_content(line):
    # Converts below line
    #  1750     2     0.723     0.751       NaN       NaN       NaN
    # to list of values

    regex = '[\w\d.-]+'
    return re.findall(regex,  line)

def berkleyearth_dataset_to_csv(be_dataset_path):
    file_name = Path(be_dataset_path).stem
    parent_dir = Path(be_dataset_path).parent
    csv_file = os.path.join(parent_dir, f'{file_name}.csv')

    if os.path.exists(csv_file):
        os.remove(csv_file)

    with open(be_dataset_path, 'r') as bf_raw, open(csv_file, 'w+') as bf_csv:
        csvout = csv.writer(bf_csv, delimiter=',')

        bf_raw_lines = bf_raw.readlines()
        comments = filter(lambda line: line.startswith('%'), bf_raw_lines)
        content = filter(lambda line: not line.startswith('%'), bf_raw_lines)

        # read last two lines of comments, because they are headers
        *_, h1, h2 = comments
        headers = berkleyearth_dataset_header(h1, h2)
        csvout.writerow(headers)

        # read content
        for numbers in content:
            values = berkleyearth_dataset_content(numbers)
            csvout.writerow(values)
