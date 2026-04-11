import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        prog="alman",
        description="CLI tools to handle alias command, custom scripts."
    )

    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show program version and exit"
    )

    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Force next decision to Confirm"
    )

    command = parser.add_subparsers( # primary command {menu, info}
        dest="command"
    )

    command.add_parser(
        "menu",
        help="Open menu page"
    )

    command_info = command.add_parser( # add info to primary command as subparsers
        "info",
        help="Show up program informations"
    )

    command_info_option = command_info.add_subparsers(
        dest="option",
        help="Specify information to print on command line"
    )

    command_info_option.add_parser(
        "status",
        help="Print program status"
    )

    command_info_option.add_parser(
        "settings",
        help="Print program settings & configuration"
    )

    command_info_option.add_parser(
        "user",
        help="Print user information and status"
    )

    parser.set_defaults(command="menu")

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()