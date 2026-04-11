import sys

def args_handler(args):
    if args.version:
        print(f"Alman 0.1.0")
        sys.exit(0)
    if args.yes:
        pass

    if args.command:
        if args.command == "menu":
            print(" ______     __         __    __     ______     __   __    ")
            print("/\\  __ \\   /\\ \\       /\\ \"-./  \\   /\\  __ \\   /\\ \"-.\\ \\  ")
            print("\\ \\  __ \\  \\ \\ \\____  \\ \\ \\-./\\ \\  \\ \\  __ \\  \\ \\ \\-.  \\ ")
            print(" \\ \\_\\ \\_\\  \\ \\_____\\  \\ \\_\\ \\ \\_\\  \\ \\_\\ \\_\\  \\ \\_\\\\\"\\_\\")
            print("  \\/_/\\/_/   \\/_____/   \\/_/  \\/_/   \\/_/\\/_/   \\/_/ \\/_/ ")
        if args.command == "info":
            if args.option == "all":
                print("All information right here")
            if args.option == "status":
                print("Status information")
            if args.option == "settings":
                print("Settings & configuration information")
            if args.option == "user":
                print("User information")