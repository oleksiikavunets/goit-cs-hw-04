import glob
import pprint
import time
from collections import defaultdict
from threading import Thread

from text_search import search_words_in_files


def search_words(*words, workers=4):
    all_files = glob.glob("data/*")
    files = [all_files[i * workers:(i + 1) * workers] for i in range((len(all_files) + workers - 1) // workers)]
    results = defaultdict(list)

    threads = [Thread(target=search_words_in_files, args=(words, fs, results)) for fs in files]
    [t.start() for t in threads]
    [t.join() for t in threads]

    return {k: sorted(v) for k, v in results.items() if v}


if __name__ == '__main__':
    print('threading module usage:\n')

    start = time.time()

    search_results = search_words('woman', 'join', 'local', 'real', 'foo')

    end = time.time()

    pprint.pprint(search_results)

    print(f'\nExecution took: {end - start}')

# threading module usage:
#
# {'join': ['data/file_0.txt', 'data/file_2.txt', 'data/file_6.txt'],
#  'local': ['data/file_0.txt',
#            'data/file_1.txt',
#            'data/file_3.txt',
#            'data/file_4.txt',
#            'data/file_5.txt'],
#  'real': ['data/file_2.txt', 'data/file_7.txt'],
#  'woman': ['data/file_0.txt', 'data/file_4.txt', 'data/file_6.txt']}
#
# Execution took: 0.00792384147644043
