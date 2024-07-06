import glob
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor

from text_search import search_words_in_files


def search_words(*words, workers=4):
    all_files = glob.glob("data/*")
    files = [all_files[i * workers:(i + 1) * workers] for i in range((len(all_files) + workers - 1) // workers)]

    futures = []

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for fs in files:
            future = pool.submit(search_words_in_files, words, fs)
            futures.append(future)

    futures_results = [future.result() for future in futures]

    results = defaultdict(dict)

    [results[word].update(result.get(word, {})) for word in words for result in futures_results]

    for word, occasions in dict(results).items():
        print(f'Word "{word}":')

        for ok, ov in occasions.items():
            print(f'    - {ok}: {ov}')

        print()


if __name__ == '__main__':
    search_words('woman', 'join', 'local', 'real', 'foo')
