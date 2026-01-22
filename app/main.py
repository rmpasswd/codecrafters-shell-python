import re
import sys, os
import stat
import subprocess
import rlcompleter, readline

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


def groom(cmd):
	g=''
	for c in cmd:
		if c==" ":
			g+=r"\c"
		elif c=="'":
			g+=r"\'"
		elif c=='"':
			g+=r"\""
		elif c=="\\":
			g+="\\"
		else:
			g+=c
	return g

def main():


	while True:
		sys.stdout.write("$ ")
		userinput = input()
		# userinput = sys.stdin.readline() # extra newline

		# match input(): # unusual behaviour, requires 2 newline and 'exit case' is invalid
		match userinput.split():  # https://docs.python.org/3/reference/compound_stmts.html#the-match-statement
			
			case ['cd', *rest]: # ['cd', ['/mnt/c/Users/Ahmad', 'Mahin/']]
				rest = [os.getenv('HOME')] if rest == ['~'] else rest
				if os.path.exists("".join(rest)):
					os.chdir("".join(rest))
				else:
					print(f"cd: {"".join(rest)}: No such file or directory")


			case [*cmd, '2>', filename ] | [*cmd, '2>>', filename ] : # ls /tmp/dir 2> lsoutput.txt
				cmd = userinput[:userinput.find("2>")] 
				returnobject = subprocess.run(f"{cmd}", shell=True, capture_output = True)
				# print(returnobject)

				# if returnobject.stderr != b'': 	# commented because we want to make the file with empty content, when there are no error
				if userinput.find("2>>"):
					with open(filename, 'a') as f:
						iterable_str = returnobject.stderr.decode('utf-8').splitlines(keepends=True) # keeps the \n line seperator in each item if keepends is true.
						f.writelines(iterable_str) #  does not put any line seperators such as \n	
				else:
					with open(filename, 'w') as f:
						iterable_str = returnobject.stderr.decode('utf-8').splitlines(keepends=True) # keeps the \n line seperator in each item if keepends is true.
						f.writelines(iterable_str) #  does not put any line seperators such as \n
				if returnobject.stdout != b'': # `cat filename notfilename` can return both an error and a standard output
					sys.stdout.write(returnobject.stdout.decode('utf-8'))
					# print(f"wrote {returnobject.stdout}")

			case [*cmd, '>', filename ] | [*cmd, '>>', filename ] | [*cmd, '1>', filename ] | [*cmd, '1>>', filename ] : # ls /tmp/dir > lsoutput.txt
				# print(cmd)
				# cmd is an array. echo 'Hello James' 1> /tmp/ becomes ['echo', "'Hello", "James'"] and prints 'Hello James' But it should print just Hello James w/o quotes

				cmd = userinput[:userinput.find("1>")] if userinput.find("1>")!=-1 else userinput[:userinput.find(">")]	

				returnobject = subprocess.run(f"{cmd}", shell=True, capture_output = True)

				# print(returnobject)
				if returnobject.returncode: # if non-zero exit code, 0 = successfull
					sys.stdout.write(returnobject.stderr.decode('utf-8'))
				# if returnobject.stdout != b'': # `cat filename notfilename` can return both an error and a standard output
				# commented to cover edge case: create empty file where there are no stdout
				if userinput.find(">>"):	
					with open(filename, 'a') as f:
						iterable_str = returnobject.stdout.decode('utf-8').splitlines(keepends=True) # keeps the \n line seperator in each item if keepends is true.
						f.writelines(iterable_str) #  does not put any line seperators such as \n
				else:
					with open(filename, 'w') as f:
						iterable_str = returnobject.stdout.decode('utf-8').splitlines(keepends=True) # keeps the \n line seperator in each item if keepends is true.
						f.writelines(iterable_str) #  does not put any line seperators such as \n
					
						# print(f"wrote {returnobject.stdout}")

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

				regexmatch = re.search(r'["\'\\]', userinput)
				if not regexmatch: # normal case with no quote or slash
					sys.stdout.write(" ".join(rest) + "\n")	

				else:
					m = userinput.lstrip("echo").strip()
					
					# Iterate through each character and define some flags for quote and spaces...
					SINGLE_QUOTE_START=False
					SINGLE_QUOTE_END=False
					INSIDE_SINGLE_QUOTE=False
					INSIDE_DOUBLE_QUOTE=False
					WHITESPACE_PRINTED=False
					
					ALREADY_ESCAPED=False 
					# for this edge case: echo "test\\"   this trailing double quote should be ignored and not affected by the preceding slash!
					
					for i,c in enumerate(m):
						if c=='\\':
							if INSIDE_SINGLE_QUOTE:
								sys.stdout.write(c)
							# elif INSIDE_DOUBLE_QUOTE:
							# 	pass
							if m[i-1]=='\\' and INSIDE_DOUBLE_QUOTE:
								sys.stdout.write(c)
								ALREADY_ESCAPED = True
							else:
								continue
						elif c=='"':
							if m[i-1]=='\\' and (not ALREADY_ESCAPED):
								sys.stdout.write(c)	
								ALREADY_ESCAPED=False
							else:
								INSIDE_DOUBLE_QUOTE = not INSIDE_DOUBLE_QUOTE
								continue
						elif c=="'":
							if m[i-1]=='\\':
								sys.stdout.write(c)
							else:
								if INSIDE_DOUBLE_QUOTE:
									sys.stdout.write(c)
									WHITESPACE_PRINTED=False
								else:
									INSIDE_SINGLE_QUOTE= not INSIDE_SINGLE_QUOTE
									WHITESPACE_PRINTED=False
						elif c==" ":
							if m[i-1]=='\\':
								sys.stdout.write(c)
							else:
								if INSIDE_SINGLE_QUOTE or INSIDE_DOUBLE_QUOTE:
									sys.stdout.write(c)
								elif not WHITESPACE_PRINTED:
									sys.stdout.write(c)
									WHITESPACE_PRINTED = not WHITESPACE_PRINTED
								else:
									continue
						else:
							sys.stdout.write(c)
							WHITESPACE_PRINTED=False
					sys.stdout.write("\n")
					# cursor=0
					# while cursor < len(m):
						
						
				#'hello     shell' 'example''world' script''test

			case ['exit']:
				sys.exit()
			
			case [firstword, *rest]: # everything else:
			# matches 'at least one word', rest can be [] and still match this case 
			# equivalent to case _: because I am always matching on a list i.e. userinput.split()
				# 	# Task is to :
				# 	# For example, if the user types custom_exe arg1 arg2, your shell should:
				# 	# Execute it with three arguments: custom_exe (the program name), arg1, and arg2
				# 	os.execvp(userinput.split()[0], userinput.split()) 
					# error: Expected prompt ("$ ") but received "" because: https://docs.python.org/3/library/os.html#:~:text=execute%20a%20new%20program%2C%20replacing%20the%20current%20process%3B%20they%20do%20not%20return
				# 	continue
				try:
					# print(f"running {firstword} with arguments {userinput.lstrip(firstword)}")
					# argstr = userinput.lstrip(firstword+' ') # "cat test.py".lstrip(cat ) becomes est.py
					argstr = userinput.removeprefix(firstword+" ")

						# firstword = groom(firstword)
					# no need to search in PATH 
					# returnobject = subprocess.run([firstword, argstr])	#  cat 'n  ote.txt' 'd  r.txt' becomes cat "'n  ote.txt' 'd  r.txt'": no such file.
					returnobject = subprocess.run(f"{userinput}", shell=True,capture_output=True)	 # https://stackoverflow.com/questions/15109665/subprocess-call-using-string-vs-using-list
					
					
					# returnobject = subprocess.run(f"{firstword} {argstr}", shell=True,capture_output=True)	 
					# print(f"trying to run: {firstword}")
					if returnobject.stdout != b'': # `cat filename notfilename` can return both an error and a standard output
						sys.stdout.write(returnobject.stdout.decode('utf-8')) # print() leaves a unnecessary newline
					else:
						assert returnobject.returncode == 0   # returncode 0  means it ran successfully. # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess.returncode

				except Exception as errname:						
					sys.stdout.write(userinput + ": command not found\n")
					# sys.stdout.write(userinput + ": command not found\n" + str(errname))

if __name__ == "__main__":
	import keyword
	keyword.kwlist.append("echo")
	keyword.kwlist.append("exit")
	readline.parse_and_bind("tab: complete")
	main()


# cat 'n  ote.txt' 'd  r.txt'