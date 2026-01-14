import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    usercmd = sys.stdin.readline()
    sys.stdout.write(f"{usercmd}: command not found")


if __name__ == "__main__":
    main()
