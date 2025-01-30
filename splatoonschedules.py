import requests
from SotredObjects import *
from datetime import datetime


def find_key(json_data: dict, key_to_find: str) -> list:
    """
        Searches for a key in a JSON object.

        Args:
            json_data (dict): The JSON object to search in.
            key_to_find (str): The key to search for.

        Returns:
            str: The value of the key if found, None otherwise.
    """

    def recursive_search(data_):
        if isinstance(data_, dict):
            for k, v in data_.items():
                if k == key_to_find:
                    yield v
                else:
                    yield from recursive_search(v)
        elif isinstance(data_, list):
            for ITEM in data_:
                yield from recursive_search(ITEM)

    return list(recursive_search(json_data))


def slice_json_by_key(json_data: dict, key_to_find: str) -> list or None:
    """
        Slice JSON file as in str by use key_to_find.

        Args:
            json_data (dict): The JSON object to search in.
            key_to_find (str): The key to search for.

        Returns:
            str: The value of the key if found, None otherwise  .
    """

    if isinstance(json_data, dict):
        if key_to_find in json_data:
            return {key_to_find: json_data[key_to_find]}
        else:
            result = []
            for k, v in json_data.items():
                if isinstance(v, (dict, list)):
                    sliced_data = slice_json_by_key(v, key_to_find)
                    if sliced_data:
                        result.append({k: sliced_data})
            return result
    elif isinstance(json_data, list):
        result = []
        for ITEM in json_data:
            if isinstance(ITEM, (dict, list)):
                sliced_data = slice_json_by_key(ITEM, key_to_find)
                if sliced_data:
                    result.append(sliced_data)
        return result
    else:
        return None


def sorter_ind(list_: list, ind1: int, ind2: int, add_point: int, num_iterations: int) -> list:
    """
    Sorts and extracts elements from a list based on specified indices and increment.

    Args:
        list_ (list): The input list to sort and extract elements from.
        ind1 (int): The initial index for the first element to extract.
        ind2 (int): The initial index for the second element to extract.
        add_point (int): The increment value to add to the indices after each iteration.
        num_iterations (int): The number of iterations to perform the extraction.

    Returns:
        list: A new list containing the extracted elements in the specified order.
    """

    new_list = []
    for i in range(num_iterations):
        new_list.append(list_[ind1])
        new_list.append(list_[ind2])
        ind1, ind2 = ind1 + add_point, ind2 + add_point
    return new_list


def iso_to_normal(iso_string: str) -> str:
    """
    Converts an ISO 8601 formatted string to a normal datetime string.

    Args:
        iso_string (str): The ISO 8601 formatted string to be converted.

    Returns:
        str: The converted datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------------------------------------------------------------------------

def get_regular_schedules() -> Link:
    MapsNamesRegular, ImagesRegular = [], []
    DATA_URl = "https://splatoon3.ink/data/schedules.json"
    RU_TRANSLATE_URL = "https://splatoon3.ink/data/locale/ru-RU.json"
    RegularLink = Link()

    response = requests.get(DATA_URl)
    data = response.json()

    temp_data = slice_json_by_key(data, "regularSchedules")

    id_list = []
    for item in temp_data:
        id_list.extend(find_key(item, "id"))
    response = requests.get(RU_TRANSLATE_URL)
    data = response.json()

    MapsNamesRegular = [find_key(data, id_list[i])[0]["name"] for i in range(len(id_list)) if
                        find_key(data, id_list[i])[0]["name"] != "Бой за район"]

    for i, value in enumerate(MapsNamesRegular):
        temp_box = Box()
        temp_box.add("GameMode", "Бой за район")
        temp_box.add("MapName", value)
        RegularLink.add(temp_box)

    images_list = []
    for item in temp_data:
        images_list.extend(find_key(item, "image"))

    ImagesRegular = [object_["url"] for object_ in images_list]

    for i, value in enumerate(ImagesRegular):
        RegularLink[i].add("MapPhoto", value)
        if i < len(RegularLink) - 1:
            RegularLink[i + 1].add("MapPhoto", value)

    return RegularLink


# ------------------------------------------------------------------------------------------------

def get_spontaneous_schedules() -> Link:
    DATA_URl = "https://splatoon3.ink/data/schedules.json"
    RU_TRANSLATE_URL = "https://splatoon3.ink/data/locale/ru-RU.json"
    mods = ["Устробол", "Бой за башню", "Бой за зоны", "Мегакарп"]

    tempMapName, tempGameMode = [], []

    response = requests.get(DATA_URl)
    data = response.json()

    temp_data = slice_json_by_key(data, "bankaraSchedules")

    id_list = []
    for item in temp_data:
        id_list.extend(find_key(item, "id"))

    images_list = []
    for item in temp_data:
        images_list.extend(find_key(item, "image"))

    ImagesRegular = [object_["url"] for object_ in images_list]

    response = requests.get(RU_TRANSLATE_URL)
    data = response.json()

    tempMapName = [find_key(data, id_list[i])[0]["name"] for i in range(len(id_list)) if
                   find_key(data, id_list[i])[0]["name"] not in mods]

    tempGameMode = [find_key(data, id_list[i])[0]["name"] for i in range(len(id_list)) if
                    find_key(data, id_list[i])[0]["name"] in mods]

    # Создание двуч дочерних и одной основной ссылки

    OpenSpontaneousSubLink = Link()
    SerialSpontaneousSubLink = Link()
    MainSpontaneousLink = Link()

    # Тип режима для Серийных карт
    SerialSpontaneousGameMode = [tempGameMode[i] for i in range(0, 24, 2)]

    for i in range(0, len(SerialSpontaneousGameMode)):
        temp_box = Box()
        temp_box.add("GameMode", SerialSpontaneousGameMode[i])
        SerialSpontaneousSubLink.add(temp_box)
        temp_box = Box()
        temp_box.add("GameMode", SerialSpontaneousGameMode[i])
        SerialSpontaneousSubLink.add(temp_box)

    # Тип режима для Открытых карт
    OpenSpontaneousGameMode = [tempGameMode[i] for i in range(24) if (i + 1) % 2 == 0]

    for i in range(0, len(OpenSpontaneousGameMode)):
        temp_box = Box()
        temp_box.add("GameMode", OpenSpontaneousGameMode[i])
        OpenSpontaneousSubLink.add(temp_box)
        temp_box = Box()
        temp_box.add("GameMode", OpenSpontaneousGameMode[i])
        OpenSpontaneousSubLink.add(temp_box)

    # Карты для Стихийного боя Серийного
    INDEXA = 0
    INDEXB = 1
    SerialSpontaneousMapsNames = sorter_ind(tempMapName, INDEXA, INDEXB, 4, 12)

    for i, value in enumerate(SerialSpontaneousMapsNames):
        SerialSpontaneousSubLink[i].add("MapName", value)

    # Карты для Стихийного боя Открытого
    INDEXA = 2
    INDEXB = 3
    OpenSpontaneousMapsNames = sorter_ind(tempMapName, INDEXA, INDEXB, 4, 12)

    for i, value in enumerate(OpenSpontaneousMapsNames):
        OpenSpontaneousSubLink[i].add("MapName", value)

    # Фотки карт для Серийного Стихийного боя
    INDEXA = 0
    INDEXB = 1
    SerialSpontaneousPhotos = sorter_ind(images_list, INDEXA, INDEXB, 4, 12)

    for i, value in enumerate(SerialSpontaneousPhotos):
        SerialSpontaneousSubLink[i].add("Photo", value)

    # Фотки карт для Открытого Стихийного боя
    INDEXA = 2
    INDEXB = 3
    OpenSpontaneousPhotos = sorter_ind(images_list, INDEXA, INDEXB, 4, 12)

    for i, value in enumerate(OpenSpontaneousPhotos):
        OpenSpontaneousSubLink[i].add("Photo", value)

    return SerialSpontaneousSubLink, OpenSpontaneousSubLink


# ------------------------------------------------------------------------------------------------

def get_unidentified_schedules() -> Link:
    DATA_URl = "https://splatoon3.ink/data/schedules.json"
    RU_TRANSLATE_URL = "https://splatoon3.ink/data/locale/ru-RU.json"
    UnidentifiedLink = Link()

    response = requests.get(DATA_URl)
    data = response.json()
    temp_data = slice_json_by_key(data, "xSchedules")

    mods = ["Устробол", "Бой за башню", "Бой за зоны", "Мегакарп"]
    UnidentifiedMapName, UnidentifiedGameMode = [], []
    id_list = []

    for item in temp_data:
        id_list.extend(find_key(item, "id"))

    response = requests.get(RU_TRANSLATE_URL)
    data = response.json()

    # Находим типы карт для Боя Х
    UnidentifiedGameMode = [find_key(data, id_list[i])[0]["name"] for i in range(len(id_list)) if
                            find_key(data, id_list[i])[0]["name"] in mods]

    for i, value in enumerate(UnidentifiedGameMode):
        temp_box = Box()
        temp_box.add("GameMode", UnidentifiedGameMode[i])
        UnidentifiedLink.add(temp_box)
        temp_box = Box()
        temp_box.add("GameMode", UnidentifiedGameMode[i])
        UnidentifiedLink.add(temp_box)

    # Находим имена карт для Боя Х
    UnidentifiedMapName = [find_key(data, id_list[i])[0]["name"] for i in range(len(id_list)) if
                           find_key(data, id_list[i])[0]["name"] not in mods]

    for i, value in enumerate(UnidentifiedMapName):
        UnidentifiedLink[i].add("MapName", value)

    # Находим фото карт для Боя Х
    images_list = []

    for item in temp_data:
        images_list.extend(find_key(item, "image"))

    for i, value in enumerate(images_list):
        UnidentifiedLink[i].add("Photo", value)

    return UnidentifiedLink


# ------------------------------------------------------------------------------------------------

def festival_schedules() -> Box:
    FestivalDate = Box()

    DATA_URL = "https://splatoon3.ink/data/festivals.json"
    RU_TRANSLATE_URL = "https://splatoon3.ink/data/locale/ru-RU.json"

    response = requests.get(DATA_URL)
    data = response.json()

    temp_date = slice_json_by_key(data, "festRecords")

    response = requests.get(RU_TRANSLATE_URL)
    data = response.json()

    nowadays_festival_text = find_key(data, find_key(temp_date, "__splatoon3ink_id")[0])
    temp_fest_start_time = find_key(temp_date, "startTime")[0]
    temp_fest_end_time = find_key(temp_date, "endTime")[0]
    nowadays_festival_photo = find_key(temp_date, "image")[0]["url"]
    nowadays_festival_start_time = f"{temp_fest_start_time[0:temp_fest_start_time.find("T")]} 03:00:00"
    nowadays_festival_end_time = f"{temp_fest_end_time[0:temp_fest_end_time.find("T")]} 03:00:00"

    FestivalDate.add("Title", nowadays_festival_text[0]["title"])
    FestivalDate.add("Teams", [nowadays_festival_text[0]["teams"][0]["teamName"],
                               nowadays_festival_text[0]["teams"][1]["teamName"],
                               nowadays_festival_text[0]["teams"][2]["teamName"]])
    FestivalDate.add("Photo", nowadays_festival_photo)
    FestivalDate.add("TimeRange", [nowadays_festival_start_time, nowadays_festival_end_time])

    return FestivalDate

