import configparser
import hashlib
import os

config = configparser.ConfigParser()
config.read('md5_matcher_config.properties')
staging_path = config.get('main', 'staging_path')
verification_path = config.get('main', "verification_path")
matcher_skip_extensions = config.get('main', "matcher_skip_extensions").split(',')
print_line_width = 150


def print_repeat(line: str):
    print(line * print_line_width)


def pretty_print_dict(input_dict: dict):
    for key, value in input_dict.items():
        print("{0:150} | {1}".format(str(key), str(value)))


def pretty_print_list(input_list: list):
    for value in input_list:
        print(value)


def calculate_md5(filename):
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def get_files_list(path):
    matches = []
    for root, dirs, files in os.walk(path):
        for basename in files:
            filename = os.path.join(root, basename)
            if len(matcher_skip_extensions) > 0 and matcher_skip_extensions[0] != '':
                if not basename.lower().endswith(tuple(matcher_skip_extensions)):
                    matches.append(filename)
            else:
                matches.append(filename)
    return matches


def build_files_tree(path_to_check):
    initial_files_list = get_files_list(path_to_check)
    files_tree = {}
    for file in initial_files_list:
        if os.path.isfile(file):
            print("found file [" + file + "] , calculating md5...", end='')
            checksum = calculate_md5(file)
            print(checksum)
            files_tree[file] = checksum
    return files_tree


def get_match(base_path_dict, path_to_find_match_dict):
    found_matches = {}
    no_match_list = []
    for v_file, v_md5 in (base_path_dict.items()):
        match_list = []
        for s_file, s_md5 in path_to_find_match_dict.items():
            if s_md5 == v_md5:
                match_list.append(s_file)
        if len(match_list) > 0:
            found_matches[v_file] = match_list
        else:
            no_match_list.append(v_file)

    return found_matches, no_match_list
