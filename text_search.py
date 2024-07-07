import re


def search(word, files_names, results):
    pattern = re.compile(r'\b(%s)\b' % word, re.IGNORECASE)

    for file_name in files_names:
        try:
            with open(file_name) as file:
                content = file.read()

                if re.search(pattern, content):
                    if word in results:
                        results[word].append(file_name)
                    else:
                        results[word] = [file_name]
        except FileNotFoundError as e:
            print(f'Error occurred when reading file {file_name}\n{e}')


def search_words_in_files(words, files, results):
    [search(word, files, results) for word in words]
