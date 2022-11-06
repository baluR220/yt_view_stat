import csv
import sys
from multiprocessing import Pool

import youtube_dl


def worker(url, item):
    return get_views(get_playlist_info(url, item))


def get_playlist_info(url, item, fn_only=False):
    ydl_options = {
        'playlist_items': f'{item}',
    }
    while True:
        try:
            with youtube_dl.YoutubeDL(ydl_options) as ydl:
                data = ydl.extract_info(
                    url, download=False, process=(not fn_only)
                )
        except youtube_dl.utils.DownloadError:
            pass
        finally:
            break
    return data


def get_views(data):
    try:
        info = [
            (data['entries'][0]['title']).replace('\xc2', ' '),
            data['entries'][0]['view_count'],
            'https://youtube.com/watch?v=' + data['entries'][0]['id']
        ]
    except IndexError:
        info = []
    return(info)


def get_filename(data):
    filename = data['title'] + '.csv'
    return(filename)


def write_to_file(data_set, filename):
    # cp1251 for windows, utf-8 for other oses
    with open(filename, 'w', encoding='cp1251') as w_file:
        file_writer = csv.writer(w_file, delimiter=';')
        # csv.field_size_limit(120)
        file_writer.writerows(data_set)


if __name__ == "__main__":
    url = sys.argv[1]
    data_set = []
    filename = get_filename(get_playlist_info(url, 1, fn_only=True))
    start = 1
    step = 5
    stop = False
    while True:
        with Pool(step) as p:
            data = ((p.starmap(
                worker, [(url, item) for item in range(start, start + step)]
            )))
        if [] in data:
            stop = True
            data = [line for line in data if line]
        data_set.extend(data)
        start += step
        if stop:
            break
    write_to_file(data_set, filename)
