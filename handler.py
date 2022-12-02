import argparse
import os
import hashlib


def get_file_format():
    file_format = input("Enter file format:\n")
    if file_format:
        return f".{file_format}"
    return None


def get_sorting_option():
    while True:
        print("Size sorting options:\n1. Descending\n2. Ascending\n")
        sorting_option = input("Enter a sorting option:\n")
        try:
            sorting_option = int(sorting_option)
            if sorting_option == 1 or sorting_option == 2:
                break
        except ValueError:
            pass
        print("\nWrong option\n")
    return sorting_option


def check_duplicates():
    print()
    while True:
        checker = input("Check for duplicates?\n")
        if checker == "yes":
            return checker
        elif checker == "no":
            return None
        else:
            print("Wrong option\n")
            continue


def hash_files(value, path):
    if value is not None:
        file = open(path, 'rb')
        hasher = hashlib.md5()
        block_size = 65536
        buf = file.read(block_size)

        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(block_size)
        file.close()
        return hasher.hexdigest()


def print_duplicates(files, value, sort):
    i = 1
    file_list = []
    for key, val in sorted(files.items(), reverse=sort):
        hash_dict = {}
        if len(val) > 1:
            print(f"\n{key} bytes")
            for v in val:
                file_hash = hash_files(value, v)
                if file_hash in hash_dict:
                    hash_dict[file_hash].append(v)
                else:
                    hash_dict[file_hash] = [v]
        for key_, val_ in hash_dict.items():
            if len(val_) > 1:
                print(f"Hash: {key_}")
                for v in val_:
                    print(f"{i}. {v}")
                    file_list.append([i, v, key])
                    i += 1
    return file_list


def find_in_list(list_, index_):
    for sub_list in list_:
        if index_ in sub_list:
            return list_.index(sub_list)


def delete_files(file_list_):
    answer = input("\nDelete files?\n")
    if answer.lower() == "no":
        exit(0)
    elif answer.lower() == "yes":
        while True:
            print("\nEnter file numbers to delete:")
            try:
                del_files = list(map(int, input().strip().split()))
            except ValueError:
                print("\nWrong format\n")
            else:
                if not len(del_files) or (max(del_files) > len(file_list_)):
                    print("\nWrong format")
                else:
                    space_freed = 0
                    for number in del_files:
                        index = find_in_list(file_list_, number)
                        os.remove(file_list_[index][1])
                        space_freed += file_list_[index][2]
                    print(f"\nTotal freed up space: {space_freed} bytes")
                    break
    else:
        print("\nWrong option")


def main():
    parser = argparse.ArgumentParser(description="List of files and folders within"
                                                 "a specific directory.")
    parser.add_argument("root_directory", nargs="?", default=None)
    args = parser.parse_args()
    if args.root_directory is None:
        print("Directory is not specified")
        exit(0)

    file_format = get_file_format()
    sorting_option = get_sorting_option()
    found_files = {}

    for root, dirs, files in os.walk(args.root_directory, topdown=False):
        for file in files:
            cur_file = os.path.join(root, file)
            extension = os.path.splitext(cur_file)[1]

            if file_format and extension != file_format:
                continue

            if not found_files.get(os.path.getsize(cur_file)):
                found_files[os.path.getsize(cur_file)] = [cur_file]
            else:
                found_files[os.path.getsize(cur_file)].append(cur_file)

    if sorting_option == 1:
        file_sizes = sorted(found_files.keys(), reverse=True)
    else:
        file_sizes = sorted(found_files.keys())

    for size in file_sizes:
        print(f"\n{size} bytes")

        for file in found_files[size]:
            print(os.path.abspath(file))

    checker = check_duplicates()

    if sorting_option == 1:
        sorting_option = True
    elif sorting_option == 2:
        sorting_option = False

    list_files = print_duplicates(found_files, checker, sorting_option)
    delete_files(list_files)


if __name__ == "__main__":
    main()
