# import requests
# from SotredObjects import *
# from datetime import datetime
#
#
# def find_key(json_data: dict, key_to_find: str) -> list:
#     """
#         Searches for a key in a JSON object.
#
#         Args:
#             json_data (dict): The JSON object to search in.
#             key_to_find (str): The key to search for.
#
#         Returns:
#             str: The value of the key if found, None otherwise.
#     """
#
#     def recursive_search(data_):
#         if isinstance(data_, dict):
#             for k, v in data_.items():
#                 if k == key_to_find:
#                     yield v
#                 else:
#                     yield from recursive_search(v)
#         elif isinstance(data_, list):
#             for ITEM in data_:
#                 yield from recursive_search(ITEM)
#
#     return list(recursive_search(json_data))
#
#
# def slice_json_by_key(json_data: dict, key_to_find: str) -> list or None:
#     """
#         Slice JSON file as in str by use key_to_find.
#
#         Args:
#             json_data (dict): The JSON object to search in.
#             key_to_find (str): The key to search for.
#
#         Returns:
#             str: The value of the key if found, None otherwise  .
#     """
#
#     if isinstance(json_data, dict):
#         if key_to_find in json_data:
#             return {key_to_find: json_data[key_to_find]}
#         else:
#             result = []
#             for k, v in json_data.items():
#                 if isinstance(v, (dict, list)):
#                     sliced_data = slice_json_by_key(v, key_to_find)
#                     if sliced_data:
#                         result.append({k: sliced_data})
#             return result
#     elif isinstance(json_data, list):
#         result = []
#         for ITEM in json_data:
#             if isinstance(ITEM, (dict, list)):
#                 sliced_data = slice_json_by_key(ITEM, key_to_find)
#                 if sliced_data:
#                     result.append(sliced_data)
#         return result
#     else:
#         return None
#
#
# def iso_to_normal(iso_string: str) -> str:
#     """
#     Converts an ISO 8601 formatted string to a normal datetime string.
#
#     Args:
#         iso_string (str): The ISO 8601 formatted string to be converted.
#
#     Returns:
#         str: The converted datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
#     """
#     return datetime.fromisoformat(iso_string.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M:%S")
#
#
# def festival_schedules() -> Box:
#     FestivalDate = Box()
#
#     DATA_URL = "https://splatoon3.ink/data/festivals.json"
#     RU_TRANSLATE_URL = "https://splatoon3.ink/data/locale/ru-RU.json"
#
#     response = requests.get(DATA_URL)
#     data = response.json()
#
#     temp_date = slice_json_by_key(data, "festRecords")
#
#     response = requests.get(RU_TRANSLATE_URL)
#     data = response.json()
#
#     nowadays_festival_text = find_key(data, find_key(temp_date, "__splatoon3ink_id")[0])
#     temp_fest_start_time = find_key(temp_date, "startTime")[0]
#     temp_fest_end_time = find_key(temp_date, "endTime")[0]
#     nowadays_festival_photo = find_key(temp_date, "image")[0]["url"]
#     nowadays_festival_start_time = f"{temp_fest_start_time[0:temp_fest_start_time.find("T")]} 03:00:00"
#     nowadays_festival_end_time = f"{temp_fest_end_time[0:temp_fest_end_time.find("T")]} 03:00:00"
#
#     FestivalDate.add("Title", nowadays_festival_text[0]["title"])
#     FestivalDate.add("Teams", [nowadays_festival_text[0]["teams"][0]["teamName"], nowadays_festival_text[0]["teams"][1]["teamName"], nowadays_festival_text[0]["teams"][2]["teamName"]])
#     FestivalDate.add("Photo", nowadays_festival_photo)
#     FestivalDate.add("TimeRange", [nowadays_festival_start_time, nowadays_festival_end_time])
#
#     return FestivalDate
#
#
# print(festival_schedules())
