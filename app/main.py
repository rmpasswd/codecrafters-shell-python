from re import sub
import sys, os
import stat
import subprocess


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
			
			case ['cd', *rest]: # ['cd', ['/mnt/c/Users/Ahmad', 'Mahin/']]
				rest = [os.getenv('HOME')] if rest == ['~'] else rest
				if os.path.exists("".join(rest)):
					os.chdir("".join(rest))
				else:
					print(f"cd: {"".join(rest)}: No such file or directory")
			

			case [*cmd, '>', filename ] | [*cmd, '1>', filename ] : # ls /tmp/dir > lsoutput.txt
				returnobj = subprocess.run(cmd, capture_output = True)
				# print(returnobj.returncode)
				if returnobj.returncode: # if non-zero exit code, 0 = successfull
					print(returnobj.stderr.decode('utf-8'))
				else:
					with open(filename, 'w') as f:
						iterable_str = returnobj.stdout.decode('utf-8').splitlines(keepends=True) # keeps the \n line seperator in each item if keepends is true.
						f.writelines(iterable_str) #  does not put any line seperators such as \n
			

			case ['pwd']:
				print(os.getcwd())
			

			case ['type',*rest]:
				if rest[0] in ['echo', 'exit', 'type', 'pwd']:
					sys.stdout.write(rest[0] + " is a shell builtin\n") 
				elif (r:= search_in_ospath(rest[0])):
					# print(r)
					sys.stdout.write(rest[0] + " is " + r + "\n") 
				else:
					sys.stdout.write(rest[0] + ": not found\n") 

			case ['echo',*rest]:

				import re
				regexmatch = re.search(r"'", usercmd)
				if not regexmatch: # normal case with no quote or slash
					sys.stdout.write(" ".join(rest) + "\n")	

				else:
					m = usercmd.lstrip("echo").strip()
					
					# Iterate through each character and define some flags for quote and spaces...
					SINGLE_QUOTE_START=False
					SINGLE_QUOTE_END=False
					INSIDE_SINGLE_QUOTE=False
					WHITESPACE_PRINTED=False

					for c in m:
						if c=="'":
							INSIDE_SINGLE_QUOTE= not INSIDE_SINGLE_QUOTE
							WHITESPACE_PRINTED=False
						elif c==" ":
							if INSIDE_SINGLE_QUOTE:
								sys.stdout.write(c)
							elif not WHITESPACE_PRINTED:
								sys.stdout.write(c)
								WHITESPACE_PRINTED = not WHITESPACE_PRINTED
							else:
								continue
						else:
							sys.stdout.write(c)
					sys.stdout.write("\n")
					# cursor=0
					# while cursor < len(m):
						
						
				#'hello     shell' 'example''world' script''test

			case ['exit']:
				sys.exit()
			
			case [othercmd, *rest]: 
			# matches 'at least one word', rest can be [] and still match this case 
			# equivalent to case _: because I am always matching on a list i.e. usercmd.split()
				# print(rest)
			# case _:
				# try:
				# 	# Task is to :
				# 	# For example, if the user types custom_exe arg1 arg2, your shell should:
				# 	# Execute it with three arguments: custom_exe (the program name), arg1, and arg2
				# 	os.execvp(usercmd.split()[0], usercmd.split()) 
					# error: Expected prompt ("$ ") but received "" because: https://docs.python.org/3/library/os.html#:~:text=execute%20a%20new%20program%2C%20replacing%20the%20current%20process%3B%20they%20do%20not%20return
				# 	continue
				# except:
				# 	pass # probably could not find the command in PATH, we wont throw any error...
				try:
					# print(f"running {othercmd} with arguments {usercmd.lstrip(othercmd)}")
					# argstr = usercmd.lstrip(othercmd+' ') # "cat test.py".lstrip(cat ) becomes est.py
					argstr = usercmd.removeprefix(othercmd+" ")
					# no need to search in PATH
					# returnobject = subprocess.run([othercmd, argstr])	#  cat 'n  ote.txt' 'd  r.txt' becomes cat "'n  ote.txt' 'd  r.txt'": no such file.
					returnobject = subprocess.run(f"{othercmd} {argstr}", shell=True,capture_output=True)	 

					assert returnobject.returncode == 0   # returncode 0  means it ran successfully. # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess.returncode
					sys.stdout.write(returnobject.stdout.decode('utf-8')) # print() leaves a unnecessary newline

				except Exception as err:						
					sys.stdout.write(usercmd + ": command not found\n")

if __name__ == "__main__":
	main()


# cat 'n  ote.txt' 'd  r.txt'