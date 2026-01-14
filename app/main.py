import sys


def main():


    while True:
        sys.stdout.write("$ ")
        usercmd = input()
        # usercmd = sys.stdin.readline() # extra newline
        sys.stdout.write(usercmd + ": command not found\n")


if __name__ == "__main__":
    main()
