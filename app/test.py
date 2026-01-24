import subprocess as s
import sys,os, stat

def load_all_exec_from_path():
	k=[]
	for p in os.getenv("PATH").split(os.pathsep):
		# print(f"scanning in: {p}")

		try:
			with os.scandir(p) as scandir_iterable:  # for d in os.scandir(eachdir): directory handler stays open until garbage collection if loop ends early
				for i in scandir_iterable:
					if i.is_file() and i.stat().st_mode & stat.S_IXUSR: # or just use convenient fun: shutil.which and shutil.is_executable()
						k.append(i.name)
						# print(os.path.join(p,i.name))
						if i.name.startswith("exit"):
							print(i.name)
		except:
			continue
	print([i for i in k if i.startswith('echo')])

# Variables to track completion state
last_tab_text = ""
last_tab_matches = []
last_tab_count = 0


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
	partial = 'exi'
	fullist = ['excelexport', 'exch', 'exec', 'exim4', 'exim_checkaccess', 'exim_id_update', 'exim_lock', 'exipick', 'expand', 'extrac32']
	
	# longest common prefix:
	lcp_list=[]
	for i in fullist:
		if i.startswith(partial):
			lcp_list.append(i)
	print(lcp_list)



if __name__=='__main__':
	# load_all_exec_from_path()
	main()