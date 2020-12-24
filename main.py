import glob
import hashlib
import fnmatch
import os
import configparser

config = configparser.ConfigParser()
config.read('md5_matcher_config.properties')
staging_path = config.get('main', 'staging_path')
verification_path = config.get('main', "verification_path")
matcher_skip_extensions = config.get('main', "matcher_skip_extensions").split(',')

print_line_width = 250


def pretty_print_dict(input_dict):
    for key, value in input_dict.items():
        print("{0:150} | {1}".format(str(key), str(value)))


def pretty_print_list(input_list):
    for value in input_list:
        print(value)


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


def calculate_md5(filename):
    md5_hash = hashlib.md5()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def find_match(staging_dict, verification_dict):
    match_dict = {}
    no_match_list = []
    for v_file, v_md5 in (verification_dict.items()):
        match_list = []
        for s_file, s_md5 in staging_dict.items():
            if s_md5 == v_md5:
                match_list.append(s_file)
        if len(match_list) > 0:
            match_dict[v_file] = match_list
        else:
            no_match_list.append(v_file)
    print('*' * print_line_width)
    print('FOUND MATCHES:')
    print('_' * print_line_width)
    pretty_print_dict(match_dict)
    print('*' * print_line_width)
    if len(no_match_list) > 0:
        print('*' * print_line_width)
        print('FILES WITHOUT ANY MATCHES:')
        print('_' * print_line_width)
        pretty_print_list(no_match_list)
    else:
        print('*' * print_line_width)
        print('ALL FILES HAVE MATCHES')
        print('*' * print_line_width)


if __name__ == '__main__':
    print("Calculating files under staging path...")
    staging = build_files_tree(staging_path)
    print("Calculating files under verification path...")
    verification = build_files_tree(verification_path)
    print('*' * print_line_width)
    print('LIST OF FOUND FILES:')
    print('_' * print_line_width)
    pretty_print_dict(staging)
    pretty_print_dict(verification)
    print('*' * print_line_width)
    find_match(staging, verification)
    quit()
