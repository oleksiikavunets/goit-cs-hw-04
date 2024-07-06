import glob
from collections import defaultdict


def search(word, files_names):
    results = defaultdict(list)

    for file_name in files_names:
        with open(file_name) as file:
            lines = file.readlines()

            for line_no, line in enumerate(lines):

                if word in line.split():
                    results[file_name].append({'line_no': line_no})

    return dict(results)


def search_words_in_files(words, files):
    results = defaultdict(dict)

    for word in words:
        result = search(word, files)

        if result:
            results[word].update(result)

    return dict(results)


# def gen_files():
#     for i in range(8):
#         text = Faker().text(1000)
#
#         with open(f'file_{i}.txt', 'w') as f:
#             f.write(text)

