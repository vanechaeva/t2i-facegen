import pickle as pc
import pandas as pd
from collections import OrderedDict

def _make_dict(text):
    max_len = 0
    word_counts = {}
    for line in text:
        line = (
            line.replace(".", " .").replace(",", " ,").replace("'", " '")
        )
        words = line.split()
        if len(words) > max_len:
            max_len = len(words)
        for word in words:
            if word not in word_counts:
                word_counts[word] = 0
        word_counts[word] += 1

    sorted_words = sorted(
        list(word_counts.keys()), key=lambda x: word_counts[x], reverse=True
    )

    word_dict = OrderedDict()
    for index, word in enumerate(sorted_words):
        word_dict[word] = index + 2

    return word_dict, word_counts, max_len

def _save_dict(word_dict, word_counts, max_len, saved_location):
    with open(saved_location, "wb") as f:
        pc.dump(word_dict, f)
        pc.dump(word_counts, f)
    with open(saved_location[:-4] + ".txt", "w") as f:
        f.write(str(max_len))

def _load_dictionary(saved_location):
    with open(saved_location, "rb") as f:
        word_dict = pc.load(f)
    with open(saved_location[:-4] + ".txt", "r") as f:
        max_len = int(f.read())
    return word_dict, max_len

def make_and_save_dict_from_source(source, data_source):
    saved_location = source + ".pkl"
    try:
        cached, max_len = _load_dictionary(saved_location)
        print(f"Используется словарь, сохраненный в {saved_location}")
        return cached, max_len
    except:
        print(f"Невозможно найти сохраненный словарь в {saved_location}\nСоздаю новый...")

        if isinstance(data_source, pd.DataFrame):
            text = data_source["text_description"].values
        elif isinstance(data_source, str):
            descr_df = pd.read_csv(data_source)
            text = descr_df["text_description"].values
        else:
            raise ValueError("Неподдерживаемый тип источника данных")

        word_dict, word_counts, max_len = _make_dict(text)
        print(f"Нашлось {len(word_dict)} уникальных слов")
        print(f"Сохраняю словарь в {saved_location}")
        print(f"Максимальная длина последовательности {max_len}")
        _save_dict(word_dict, word_counts, max_len, saved_location)

        return word_dict, max_len