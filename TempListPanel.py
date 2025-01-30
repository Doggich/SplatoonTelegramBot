from os import system
from os import name as sys_name


def flush() -> int:
    return system("cls") if sys_name == "nt" else system("clear")


def open_temp(path: str) -> list:
    waste_symbols = ["|", "aka:", "(", ")"]
    with open(path, "r") as data:
        info_list = []
        for line in data:
            cleaned_line = line
            for symbol in waste_symbols:
                cleaned_line = cleaned_line.replace(symbol, "")
            words = cleaned_line.split()
            info_list.append(words)
    return info_list


def remove_duplicates(lst: list) -> list:
    original_list: list = []
    id_set: set = set()
    for elem in lst:
        for subelem in elem:
            temp_elem: str = subelem
            if temp_elem.isdigit():
                if temp_elem not in id_set:
                    original_list.append(elem)
                    id_set.add(temp_elem)
    return original_list


def show(lst: list) -> None:
    for index_, elem in enumerate(lst):
        print(f"{index_} | {str(elem)}")


def write_in(msg: list) -> None:
    with open("BL.txt", "a") as data:
        data.write(f"{msg[0]} {msg[1]} {msg[2]} {msg[3]}\n")
        data.close()


def add_in_black_list(lst: list, wrong_index: int) -> None:
    for ind1ex_, elem in enumerate(lst):
        if index_ == wrong_index:
            write_in(elem)


loop = True

while loop:
    flush()
    temp_ord = open_temp("tempList.txt")
    print("---" * 10)
    print("Check orders (1)")
    print("Check with formatted (2)")
    print("Add orders in Black List (3)")
    print("Close program (4)")
    print("---" * 10)
    act = input(">> ")
    if act == "1":
        show(temp_ord)
        input("...")
    elif act == "2":
        show(remove_duplicates(temp_ord))
        input("...")
    elif act == "3":
        index = input("Enter a index>> ")
        add_in_black_list(temp_ord, index)
        print("Successfully upload!!!")
    elif act == "4":
        loop = False
