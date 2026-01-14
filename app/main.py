import sys


def search_in_ospath(st):
    import os,stat
    dirlist = os.environ["PATH"].split(os.pathsep) # if the PATH is set to /dir1:/dir2:/dir3
    for eachdir in dirlist:
        # list the files in eachdir and find the matching name
        # print(f"looking in {eachdir}")
        # os.listdir(eachdir)
        with os.scandir(eachdir) as scandir_iterable:  # for d in os.scandir(eachdir): directory handler stays open until garbage collection if loop ends early
            for i in scandir_iterable:
                if i.is_file() and i.name == st and i.stat().st_mode & stat.S_IXUSR:
                    return eachdir + "/" + i.name # the path of the executable
                else:
                    continue # keep looking for executable
            # if os.access(path, os.X_OK): # alternate way to check if a path is executable...
    return False


def main():


    while True:
        sys.stdout.write("$ ")
        usercmd = input()
        # usercmd = sys.stdin.readline() # extra newline

        # match input(): # unusual behaviour, requires 2 newline and exit case invalid
        match usercmd.split():  # https://docs.python.org/3/reference/compound_stmts.html#the-match-statement
            case ['type',*rest]:
                if rest[0] in ['echo', 'exit', 'type']:
                    sys.stdout.write(rest[0] + " is a shell builtin\n") 
                elif (r:= search_in_ospath(rest[0])):
                    sys.stdout.write(rest[0] + " is " + r + "\n") 
                else:
                    sys.stdout.write(rest[0] + ": not found\n") 
            case ['echo',*rest]:
                sys.stdout.write(" ".join(rest) + "\n")
            case ['exit']:
                sys.exit()
            case _:
                sys.stdout.write(usercmd + ": command not found\n")

if __name__ == "__main__":
    main()

 