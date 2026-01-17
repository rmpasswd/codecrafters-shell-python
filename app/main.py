import sys, os
import stat

def search_in_ospath(st):
    # import os,stat
    dirlist = os.environ["PATH"].split(os.pathsep) # if the PATH is set to /dir1:/dir2:/dir3
    for eachdir in dirlist:
        # list the files in eachdir and find the matching name
        # print(f"looking in {eachdir}")
        # os.listdir(eachdir)
        try:
            with os.scandir(eachdir) as scandir_iterable:  # for d in os.scandir(eachdir): directory handler stays open until garbage collection if loop ends early
                for i in scandir_iterable:
                    if i.name == st  and  i.is_file()  and i.stat().st_mode & stat.S_IXUSR: # or just use convenient fun: shutil.which and shutil.is_executable()
                        return eachdir + "/" + i.name # the path of the executable
                    else:
                        continue # keep looking for executable
                # if os.access(path, os.X_OK): # alternate way to check if a path is executable...
        except:
            # plot twist: Linux allows non-existent directories in PATH. hence looking for a dir will throw error

            continue
    return False


def main():


    while True:
        sys.stdout.write("$ ")
        usercmd = input()
        # usercmd = sys.stdin.readline() # extra newline

        # match input(): # unusual behaviour, requires 2 newline and 'exit case' is invalid
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
            case [othercmd, *rest]:
                os.execlp(othercmd,*rest)
            case _:
                try:
                    # Task is to :
                    # For example, if the user types custom_exe arg1 arg2, your shell should:
                    # Execute it with three arguments: custom_exe (the program name), arg1, and arg2
                    # [cmd, *args] = usercmd.split()
                    os.execvp(usercmd.split()[0], usercmd.split())
                except:
                    pass # probably could not find the command in PATH
                sys.stdout.write(usercmd + ": command not found\n")

if __name__ == "__main__":
    main()

 

