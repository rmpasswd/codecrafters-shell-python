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
if __name__=='__main__':
	load_all_exec_from_path()