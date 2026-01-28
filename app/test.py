import subprocess  
import sys,os, stat
import shlex
import signal

# keep this
def get_longest_common_prefix(strings):
	"""Get the longest common prefix of a list of strings."""
	if not strings:
		return ""
	if len(strings) == 1:
		return strings[0]
		
	prefix = strings[0]
	for string in strings[1:]:
		# Find the length of common prefix
		length = 0
		for i, (c1, c2) in enumerate(zip(prefix, string)):
			if c1 != c2:
				break
			length = i + 1
		
		# Update prefix to common part
		prefix = prefix[:length]
		if not prefix:
			break
			
	return prefix

def main():

	# cmd  = '''echo -e "raspberry grape\npear strawberry\nmango blueberry\npineapple banana\norange apple" '''
	# cmd = '''cat /tmp/dog/file-41'''
	cmd ='''echo -e "strawberry apple\ngrape pear\nbanana blueberry\nraspberry mango\npineapple orange" > "/tmp/cow/file-46"'''
	# returnobject = os.execvp("bash -c", ["echo -e"] + cmd.split()[1:])

	try:
		returnobject = subprocess.run(["/usr/bin/bash","-c" , cmd], capture_output=True, timeout=2)

	except:
		returnobject.send_signal(signal.SIGINT)
	print(returnobject.stdout.decode())


	# print(returnobject)


def runpipes(beforepipe,afterpipe):
	# seperate function because
	# Only one "*" pattern allowed in a pattern. case [*beforepipe, "|", *afterpipe] is invalid

	import signal
	p1 = subprocess.Popen([beforepipe.split()[0], *beforepipe.split()[1:]], stdout=subprocess.PIPE)
	try:
		# p1.wait(timeout=1)
		pass
	except Exception as TimeoutExpired:
		p1.send_signal(signal.SIGINT)
	except:
		sys.stdout.write("command not found, inside runpipe\n")

	# print(f"p1 out: {p1.stdout.read()}")   # io.Bufferedreader

	p2 = subprocess.Popen([afterpipe.split()[0], *afterpipe.split()[1:]], stdin=subprocess.PIPE)
	r = p2.communicate(p1.stdout.read())
	# print(r) # automatically printed by 'communicate' mehtod.
	# p2.wait(timeout=3)

if __name__=='__main__':
	# load_all_exec_from_path()
	runpipes()