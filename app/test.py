import subprocess as s
import sys

# r = s.run(["python3", "--version"])	# ignore pyright error

cmd="cat /tmp/w asfdasdf"
# cmd2="cat /tmp/p"
# r= s.run([*cmd],  capture_output=True)

r = s.run(f"{cmd}", shell=True,capture_output=True)	 # https://stackoverflow.com/questions/15109665/s-call-using-string-vs-using-list
# r = s.run(f"{cmd2}", shell=True,capture_output=True)	 # https://stackoverflow.com/questions/15109665/subprocess-call-using-string-vs-using-list

print(r)
sys.stdout.write("stdout:" + r.stdout.decode('utf-8'))
sys.stdout.write("stderr:" + r.stderr.decode('utf-8'))

print()