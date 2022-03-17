from lib.util import pretty_print_dict, pretty_print_list, build_files_tree, staging_path, verification_path, get_match
from lib.util import print_repeat


def find_match(staging_dict, verification_dict):
    if len(staging_dict) > 0:
        if len(verification_dict) > 0:
            print_repeat('=')
            print('LOOKING FOR MATCHES BETWEEN verification_path and staging_path:')
            v_found_matches, v_no_matches = get_match(verification_dict, staging_dict)

            if len(v_found_matches) > 0:
                print_repeat('-')
                print('FOUND MATCHES:')
                pretty_print_dict(v_found_matches)

            if len(v_no_matches) == 0:
                print_repeat('-')
                print('VERIFICATION PATH is OK!')
                print('ALL FILES FROM VERIFICATION PATH HAVE MATCHES IN STAGING PATH!')

            print_repeat('=')
            print('LOOKING FOR MATCHES BETWEEN staging_path and verification_path:')
            s_found_matches, s_no_matches = get_match(staging_dict, verification_dict)

            if len(s_found_matches) > 0:
                print_repeat('-')
                print('FOUND MATCHES:')
                pretty_print_dict(s_found_matches)

            if len(s_no_matches) == 0:
                print_repeat('-')
                print('STAGING PATH is OK!')
                print('ALL FILES FROM STAGING PATH HAVE MATCHES IN VERIFICATION PATH!')

            # FINAL VERDICT
            if len(s_no_matches) == 0 and len(v_no_matches) == 0:
                print()
                print_repeat('*')
                print('FINAL VERDICT:')
                print('EVERYTHING is OK!')
                print('ALL FILES FROM STAGING PATH HAVE MATCHES IN VERIFICATION PATH')
                print('ALL FILES FROM VERIFICATION PATH HAVE MATCHES IN STAGING PATH')
                print_repeat('*')
                print()
            else:
                if not len(v_no_matches) == 0:
                    print()
                    print_repeat('*')
                    print('FINAL VERDICT:')
                    print('NOT OK!!! NOT ALL FILES FROM VERIFICATION PATH HAVE MATCHES IN STAGING PATH')
                    print('FILES WITHOUT ANY MATCHES:')
                    pretty_print_list(v_no_matches)
                    print_repeat('*')
                    print()

                if not len(s_no_matches) == 0:
                    print()
                    print_repeat('*')
                    print('NOT OK!!! NOT ALL FILES FROM STAGING PATH HAVE MATCHES IN VERIFICATION PATH')
                    print('FILES WITHOUT ANY MATCHES:')
                    pretty_print_list(s_no_matches)
                    print_repeat('*')
                    print()

        else:
            print_repeat('*')
            print('NOT OK!!! NO files were found at directory', verification_path)
    else:
        print_repeat('*')
        print('NOT OK!!! NO files were found at directory', staging_path)


if __name__ == '__main__':
    print("Calculating files under staging path...")
    staging = build_files_tree(staging_path)
    print("Calculating files under verification path...")
    verification = build_files_tree(verification_path)
    print_repeat('=')
    print('LIST OF FOUND FILES AND THEIR MD5:')
    pretty_print_dict(staging)
    pretty_print_dict(verification)
    find_match(staging, verification)
    quit()
