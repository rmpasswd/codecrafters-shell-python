import subprocess as s
import sys

# r = s.run(["python3", "--version"])	# ignore pyright error

cmd0="export PATH=/tmp/:$PATH"
cmd="cat /tmp/rat/banana"
# cmd="asdf.sh"

r = s.run(f"{cmd}", shell=True, capture_output=True)

# r = s.run(f"{cmd0}", shell=True,capture_output=True)	 # https://stackoverflow.com/questions/15109665/s-call-using-string-vs-using-list
# r = s.run(f"{cmd}", shell=True,capture_output=True)	 # https://stackoverflow.com/questions/15109665/s-call-using-string-vs-using-list

print(r)

