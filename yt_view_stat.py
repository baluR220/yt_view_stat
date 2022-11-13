import csv
import sys
from datetime import datetime
from multiprocessing import Pool

import youtube_dl


def worker(url_gen):
    url = 'https://www.youtube.com/watch?v=' + url_gen['url']
    while True:
        try:
            data = get_views(get_info(url))
        except Exception:
            pass
        else:
            break
    return(data)


def get_info(url):
    ydl_options = {
        'youtube_include_dash_manifest': False,
        'socket_timeout': 5,
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        data = ydl.extract_info(
            url, download=False, process=False
        )
    return data


def get_views(data):
    info = [
        (data['title']).replace('\xc2', ' '),
        data['view_count'],
        'https://youtube.com/watch?v=' + data['id']
    ]
    return(info)


def get_filename(data):
    filename = data['title'] + '.csv'
    gen = data['entries']
    return(filename, gen)


def write_to_file(data_set, filename):
    # cp1251 for windows, utf-8 for other oses
    with open(filename, 'w', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=';')
        # csv.field_size_limit(120)
        file_writer.writerows(data_set)


if __name__ == "__main__":
    t_start = datetime.now()
    url = sys.argv[1]
    filename, gen = get_filename(get_info(url))
    with Pool() as p:
        data_set = p.map(
            worker, gen
        )
    print(len(data_set))
    write_to_file(data_set, filename)
    print(datetime.now() - t_start)
