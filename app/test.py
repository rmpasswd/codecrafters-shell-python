import subprocess as s
import sys

# r = s.run(["python3", "--version"])	# ignore pyright error

cmd=['echo', "'Hello", "James'"]
r= s.run([*cmd],  capture_output=True)


# r= s.run(f"{cmd}",shell=True,  capture_output=True)

# print(r)
sys.stdout.write(r.stdout.decode('utf-8'))

