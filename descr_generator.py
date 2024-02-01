import random
import pandas as pd
import numpy as np

from tqdm import tqdm

random.seed(0)
face_structure = {"Пухлый", "Двойной_подбородок", "Овальное_лицо", "Высокие_скулы"}
facial_hair = {"Щетина", "Козлиную_бородку", "Усы", "Бакенбарды"}

hairstyle = {
    "Лысый",
    "Прямые_волосы",
    "Волнистые_волосы",
    "Черные_волосы",
    "Светлые_волосы",
    "Коричневые_волосы",
    "Серые_волосы",
    "Редеющие_волосы",
}

facial_features = {
    "Большие_губы",
    "Большой_нос",
    "Острый_нос",
    "Узкие_глаза",
    "Поднятые_брови",
    "Густые_брови",
    "Приоткрытый_рот",
}

appearance = {
    "Молодо",
    "Привлекательно",
    "Улыбается",
    "Бледная_кожа",
    "Много_косметики_на_лице",
    "Розовые_щеки",
}

accessories = {
    "Носит_серьги",
    "Носит_шляпу",
    "Носит_помаду",
    "Носит_колье",
    "Носит_галстук",
    "Очки",
}

def generate_face_structure(face_attributes, is_male):

    features = {
        "Пухлый": ["пухлое лицо", "пухленький", "слегка полноватое лицо"],
        "Высокие_скулы": ["высокие скулы", "довольно высокие скулы"],
        "Овальное_лицо": ["овальцое лицо"],
        "Двойной_подбородок": ["двойной подбородок"],
    }

    if is_male:
        sentence = random.choice(["Мужчина"])
    else:
        sentence = random.choice(["Женщина"])

    if len(face_attributes) == 1:
        attribute = random.choice(features[face_attributes[0]])
        if face_attributes[0] != "Пухлый":
            sentence += " имеет"
        return sentence + " " + attribute + "."
    else:
        for i in range(len(face_attributes)):
            attribute = random.choice(features[face_attributes[i]])

            if i < len(face_attributes) - 1:
                if face_attributes[i] != "Пухлый":
                    sentence += " имеет"
                sentence += " " + attribute + ","
            else:
                sentence = sentence[:-1]
                sentence += " и"
                if face_attributes[i - 1] == "Пухлый":
                    sentence += " имеет"
                sentence += " " + attribute + "."

        return sentence


def generate_facial_hair(facial_hair_attributes, is_male):
    build = ["имеет"]

    sentence = "Он" if is_male else "Она"

    if len(facial_hair_attributes) == 1:
        attribute = (
            facial_hair_attributes[0].lower()
            if facial_hair_attributes[0] != "Щетина"
            else "щетину"
        )
        conj = random.choice(build)

        if attribute == "бакенбарды":
            conj = "имеет"

        return sentence + " " + conj + " " + attribute + "."
    else:
        for i in range(len(facial_hair_attributes)):
            attribute = (
                facial_hair_attributes[i].lower()
                if facial_hair_attributes[i] != "Щетина"
                else "щетина"
            )
            conj = random.choice(build)

            if attribute == "бакенбарды":
                conj = "имеет"

            if i < len(facial_hair_attributes) - 1:
                sentence = sentence + " " + conj + " " + attribute + ","
            else:
                sentence = sentence[:-1]
                sentence = sentence + " и " + conj + " " + attribute + "."
        return sentence


def generate_hairstyle(hairstyle_attributes, is_male):
    hair_type = {"Лысый", "Прямые_волосы", "Волнистые_волосы", "Редеющие_волосы"}

    arranged_attributes = []
    colours = list(set(hairstyle_attributes) - hair_type)

    if len(colours) > 1:
        colour = ""
        for i, _colour in enumerate(colours):
            if i == 0:
                _colour = _colour.lower().split("_")[0] + "-"
            _colour = _colour.lower().split("_")[0]
            colour += _colour + " "
        arranged_attributes.append(
            colour.strip()
        )
    elif len(colours) == 1:
        colour = colours[0].lower().split("_")[0]
        arranged_attributes.append(colour)
    style = set(hairstyle_attributes) & {"Прямые_волосы", "Волнистые_волосы"}
    arranged_attributes.extend(list(style))
    bald_rec = set(hairstyle_attributes) & {"Редеющие_волосы", "Лысый"}
    arranged_attributes.extend(list(bald_rec))

    if len(arranged_attributes) == 1:
        attribute = arranged_attributes[0].lower().split("_")[0]
        if attribute == "лысый":
            return "Он лысый." if is_male else "Она лысая."
        if random.random() <= 0.5:
            sentence = "Его" if is_male else "Её"
            return sentence + " волосы " + attribute + "."
        else:
            sentence = "Он" if is_male else "Она"
            return sentence + " имеет " + attribute + " волосы."

    if random.random() <= 0.5:
        sentence = "Его" if is_male else "Её"
        sentence += " волосы"
        for i, attribute in enumerate(arranged_attributes):
            attribute = attribute.lower().split("_")[0]
            if len(arranged_attributes) - 1 == i:
                sentence = sentence[:-1]
                if attribute == "лысый":
                    attribute = "он" if is_male else "она"
                    attribute += (
                        "" + " лысеет"
                    )
                    return sentence + " и " + attribute + "."
                return sentence + " и " + attribute + "."
            sentence += " " + attribute + ","
    else:
        sentence = "Он" if is_male else "Она"
        sentence += " имеет"
        for i, attribute in enumerate(arranged_attributes):
            attribute = attribute.lower().split("_")[0]
            if len(arranged_attributes) - 1 == i:
                sentence = sentence[:-1]
                if attribute == "лысый":
                    sentence += " волосы"
                    attribute = "он" if is_male else "она"
                    attribute += (
                        "" + " лысеет"
                    )
                    return sentence + " и " + attribute + "."
                return sentence + " и " + attribute + " волосы."
            sentence += " " + attribute + ","


def generate_facial_features(facial_features, is_male):
    sentence = "Он" if is_male else "Она"
    sentence += " имеет"

    def nose_and_mouth(attribute):
        if attribute == "большой нос" or attribute == "острый нос":
            return attribute
        elif attribute == "приоткрытый рот":
            return "слегка приоткрытый рот"
        return attribute

    if len(facial_features) == 1:
        attribute = nose_and_mouth(" ".join(facial_features[0].lower().split("_")))
        return sentence + " " + attribute + "."

    for i, attribute in enumerate(facial_features):
        attribute = nose_and_mouth(" ".join(attribute.lower().split("_")))

        if i == len(facial_features) - 1:
            sentence = sentence[:-1]
            sentence += " и " + attribute + "."
        else:
            sentence += " " + attribute + ","

    return sentence


def generate_appearance(appearance, is_male):
    is_smiling = "Улыбается" in appearance
    smile_begin = False if not is_smiling else True if random.random() <= 0.5 else False
    qualities = list(set(appearance) & {"Молодо", "Привлекательно"})
    extras = list(set(appearance) & {"Бледная_кожа", "Много_косметики_на_лице", "Розовые_щеки"})

    sentence = (
        random.choice(["Он", "Мужчина"])
        if is_male
        else random.choice(["Она", "Женщина"])
    )

    if is_smiling and len(qualities) == 0 and len(extras) == 0:
        return sentence + " улыбается."

    if is_smiling and smile_begin:
        sentence += " улыбается"
        sentence += "," if len(qualities) > 0 or len(extras) > 1 else ""


    if len(qualities) == 1:
        if len(extras) == 0 and smile_begin:
            sentence = sentence[:-1]
            sentence += " и"
        sentence += (
            random.choice([" выглядит", " смотрится"]) + " " + qualities[0].lower()
        )
        sentence += (
            "," if len(extras) > 1 or (is_smiling and not smile_begin) else ""
        )
    elif len(qualities) > 1:
        sentence += random.choice([" выглядит", " смотрится"])
        for i in range(len(qualities)):
            attribute = qualities[i].lower()

            if i == len(qualities) - 1 and len(extras) == 0:
                sentence = sentence[:-1]
                sentence += " и " + attribute
            else:
                sentence += " " + attribute + ","


    if is_smiling and not smile_begin:
        if len(extras) == 0:
            sentence = sentence.replace(",", " и")
        sentence += " улыбается"
        sentence += "," if len(extras) > 1 else ""

    extras = [" ".join(e.split("_")) for e in extras]

    if len(extras) == 0:
        return sentence + "."
    elif len(extras) == 1:
        if len(qualities) > 0 or is_smiling:
            if len(qualities) > 1 and ((is_smiling and smile_begin) or not is_smiling):
                sentence = sentence[:-1]
            sentence += " и"
        return sentence + " у неё " + extras[0].lower() + "."
    else:
        sentence += " у неё"
        for i in range(len(extras)):
            attribute = extras[i].lower()

            if i == len(extras) - 1:
                sentence = sentence[:-1]
                sentence += " и " + attribute
            else:
                sentence += " " + attribute + ","

        return sentence + "."


def generate_accessories(accessories, is_male):
    sentence = "Он" if is_male else "Она"
    sentence += " носит"

    def necktie_and_hat(attribute):
        if attribute == "галстук" or attribute == "шляпу" or attribute == "колье":
            return " " + attribute
        return attribute

    if len(accessories) == 1:
        attribute = (
            accessories[0].lower()
            if accessories[0] == "Очки"
            else necktie_and_hat(accessories[0].lower().split("_")[1])
        )
        return sentence + " " + attribute + "."

    for i, attribute in enumerate(accessories):
        attribute = (
            attribute.lower()
            if attribute == "Очки"
            else necktie_and_hat(attribute.lower().split("_")[1])
        )

        if i == len(accessories) - 1:
            sentence = sentence[:-1]
            sentence += " и " + attribute + "."
        else:
            sentence += " " + attribute + ","

    return sentence


def generate_one_to_one_caption(df, path="dataset/text_descr_celeba.csv"):
    new_dict = {"image_id": [], "text_description": []}

    for i in tqdm(df.index):
        image_id = df.loc[i, "image_id"]

        face_structure_arr = []
        facial_hair_arr = []
        hairstyle_arr = []
        facial_features_arr = []
        appearance_arr = []
        accessories_arr = []
        is_male = False

        description = ""

        for attr in df.loc[i, "attributes"]:

            if attr in face_structure:
                face_structure_arr.append(attr)

            elif attr in facial_hair:
                facial_hair_arr.append(attr)

            elif attr in hairstyle:
                hairstyle_arr.append(attr)

            elif attr in facial_features:
                facial_features_arr.append(attr)

            elif attr in appearance:
                appearance_arr.append(attr)

            elif attr in accessories:
                accessories_arr.append(attr)

            elif attr == "Мужчина":
                is_male = True

        if face_structure_arr != []:
            face_structure_txt = generate_face_structure(face_structure_arr, is_male)
            description += face_structure_txt + " "

        if facial_hair_arr != []:
            facial_hair_txt = generate_facial_hair(facial_hair_arr, is_male)
            description += facial_hair_txt + " "

        if hairstyle_arr != []:
            hairstyle_txt = generate_hairstyle(hairstyle_arr, is_male)
            description += hairstyle_txt + " "

        if facial_features_arr != []:
            facial_features_txt = generate_facial_features(facial_features_arr, is_male)
            description += facial_features_txt + " "

        if appearance_arr != []:
            appearance_txt = generate_appearance(appearance_arr, is_male)
            description += appearance_txt + " "

        if accessories_arr != []:
            accessories_txt = generate_accessories(accessories_arr, is_male)
            description += accessories_txt + " "

        if description == "":
            if is_male:
                description = (
                    "Мы видим " + random.choice(["мужчину"]) + "."
                )
            else:
                description = (
                    "Мы видим " + random.choice(["женщину"]) + "."
                )

        new_dict["image_id"].append(image_id)
        new_dict["text_description"].append(description.strip())

    pd.DataFrame(data=new_dict).to_csv(path, index=False)


def generate_one_to_N_caption(df, N=5, dataset_size=10_000):
    new_dict = {"image_id": [], "text_description": []}

    for i in tqdm(range(dataset_size)):

        image_id = df.loc[i, "image_id"]
        total_description = ""

        for j in range(N):

            face_structure_arr = []
            facial_hair_arr = []
            hairstyle_arr = []
            facial_features_arr = []
            appearance_arr = []
            accessories_arr = []
            is_male = False

            description = ""

            for attr in df.loc[i, "attributes"]:

                if attr in face_structure:
                    face_structure_arr.append(attr)

                elif attr in facial_hair:
                    facial_hair_arr.append(attr)

                elif attr in hairstyle:
                    hairstyle_arr.append(attr)

                elif attr in facial_features:
                    facial_features_arr.append(attr)

                elif attr in appearance:
                    appearance_arr.append(attr)

                elif attr in accessories:
                    accessories_arr.append(attr)

                elif attr == "Мужчина":
                    is_male = True

            if face_structure_arr != []:
                face_structure_txt = generate_face_structure(
                    face_structure_arr, is_male
                )
                description += face_structure_txt + " "

            if facial_hair_arr != []:
                facial_hair_txt = generate_facial_hair(facial_hair_arr, is_male)
                description += facial_hair_txt + " "

            if hairstyle_arr != []:
                hairstyle_txt = generate_hairstyle(hairstyle_arr, is_male)
                description += hairstyle_txt + " "

            if facial_features_arr != []:
                facial_features_txt = generate_facial_features(
                    facial_features_arr, is_male
                )
                description += facial_features_txt + " "

            if appearance_arr != []:
                appearance_txt = generate_appearance(appearance_arr, is_male)
                description += appearance_txt + " "

            if accessories_arr != []:
                accessories_txt = generate_accessories(accessories_arr, is_male)
                description += accessories_txt + " "

            if description == "":
                if is_male:
                    description = (
                        "Мы видим "
                        + random.choice(["мужчину", "парня"])
                        + "."
                    )
                else:
                    description = (
                        "Мы видим " + random.choice(["женщину", "даму", "девушку"]) + "."
                    )

            total_description += description + "\n"

        new_dict["image_id"].append(image_id)
        new_dict["text_description"].append(total_description.strip())

    pd.DataFrame(data=new_dict).to_csv(
        f"dataset/text_{N}_descr_celeba.csv", index=False, encoding="utf-8-sig"
    )
def generate_random_captions(df, path="dataset/text_descr_celeba.csv"):
    new_dict = {"image_id": [], "text_description": []}

    for i in tqdm(df.index):

        image_id = df.loc[i, "image_id"]

        face_structure_arr = []
        facial_hair_arr = []
        hairstyle_arr = []
        facial_features_arr = []
        appearance_arr = []
        accessories_arr = []
        is_male = False

        description = ""

        for attr in df.loc[i, "attributes"]:
            if attr in face_structure:
                face_structure_arr.append(attr)

            elif attr in facial_hair:
                facial_hair_arr.append(attr)

            elif attr in hairstyle:
                hairstyle_arr.append(attr)

            elif attr in facial_features:
                facial_features_arr.append(attr)

            elif attr in appearance:
                appearance_arr.append(attr)

            elif attr in accessories:
                accessories_arr.append(attr)

            elif attr == "Мужчина":
                is_male = True

        random_func_list = []

        if face_structure_arr != []:
            random_func_list.append(generate_face_structure)
        if facial_hair_arr != []:
            random_func_list.append(generate_facial_hair)
        if hairstyle_arr != []:
            random_func_list.append(generate_hairstyle)
        if facial_features_arr != []:
            random_func_list.append(generate_facial_features)
        if appearance_arr != []:
            random_func_list.append(generate_appearance)
        if accessories_arr != []:
            random_func_list.append(generate_accessories)

        random.shuffle(random_func_list)

        for func in random_func_list:
            if func == generate_face_structure:
                face_structure_txt = generate_face_structure(face_structure_arr, is_male)
                description += face_structure_txt + " "

            if func == generate_facial_hair:
                facial_hair_txt = generate_facial_hair(facial_hair_arr, is_male)
                description += facial_hair_txt + " "

            if func == generate_hairstyle:
                hairstyle_txt = generate_hairstyle(hairstyle_arr, is_male)
                description += hairstyle_txt + " "

            if func == generate_facial_features:
                facial_features_txt = generate_facial_features(facial_features_arr, is_male)
                description += facial_features_txt + " "

            if func == generate_appearance:
                appearance_txt = generate_appearance(appearance_arr, is_male)
                description += appearance_txt + " "

            if func == generate_accessories:
                accessories_txt = generate_accessories(accessories_arr, is_male)
                description += accessories_txt + " "

        if description == "":
            if is_male:
                description = (
                        "Мы видим " + random.choice(["мужчину"]) + "."
                )
            else:
                description = (
                        "Мы видим " + random.choice(["женщину"]) + "."
                )
        new_dict["image_id"].append(image_id)
        new_dict["text_description"].append(description.strip())

    pd.DataFrame(data=new_dict).to_csv("dataset/text_shuffle_descr_celeba.csv", index=False, encoding="utf-8-sig")
if __name__ == "__main__":
    df = pd.read_csv("dataset/list_attr_celeba.csv", encoding='cp1251')

    cols = np.array(df.columns)
    b = df.values == 1
    df["attributes"] = [cols[(row_index)] for row_index in b]

    generate_one_to_N_caption(df)
    generate_one_to_one_caption(df)
    generate_random_captions(df)