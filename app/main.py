import sys


def main():


    while True:
        sys.stdout.write("$ ")
        usercmd = input()
        # usercmd = sys.stdin.readline() # extra newline

        # match input(): # unusual behaviour, requires 2 newline and exit case invalid
        match usercmd.split():
            case ['echo',*rest]:
                sys.stdout.write(" ".join(rest) + "\n")
            case ['exit']:
                sys.exit()
            case _:
                sys.stdout.write(usercmd + ": command not found\n")


if __name__ == "__main__":
    main()
