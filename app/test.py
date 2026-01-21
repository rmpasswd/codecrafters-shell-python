import subprocess as s
import sys

# r = s.run(["python3", "--version"])	# ignore pyright error
cmd="ls ."
r= s.run(f"{cmd}",shell=True,  capture_output=True)

print(r)
sys.stdout.write(r.stdout.decode('utf-8'))

