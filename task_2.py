import glob
import pprint
import time
from multiprocessing import Process, Manager

from text_search import search_words_in_files


def search_words(*words, workers=4):
    all_files = glob.glob("data/*")
    files = [all_files[i * workers:(i + 1) * workers] for i in range((len(all_files) + workers - 1) // workers)]

    with Manager() as manager:
        prepared_dict = {word: manager.list() for word in words}
        results = manager.dict(prepared_dict)

        processes = [Process(target=search_words_in_files, args=(words, fs, results)) for fs in files]
        [p.start() for p in processes]
        [p.join() for p in processes]

        return {k: sorted(v) for k, v in results.items() if v}


if __name__ == '__main__':
    print('multiprocessing module usage:\n')

    start = time.time()

    search_results = search_words('woman', 'join', 'local', 'real', 'foo')

    end = time.time()

    pprint.pprint(search_results)

    print(f'\nExecution took: {end - start}')

# multiprocessing module usage:
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
# Execution took: 0.5290570259094238
