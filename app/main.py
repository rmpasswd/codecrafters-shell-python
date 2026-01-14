import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    usercmd = input()
    # usercmd = sys.stdin.readline() # extra newline
    sys.stdout.write(usercmd + ": command not found\n")


if __name__ == "__main__":
    main()
