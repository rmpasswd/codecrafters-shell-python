## Overview
**Python solutions to the ["Build Your Own Shell" Challenge](https://app.codecrafters.io/courses/shell/overview).**

A (POSIX compliant) shell capable of: 
- interpreting shell commands,
- running external programs and builtin commands like cd, pwd, echo and more.
- shell command parsing, REPLs, builtin commands, and more.
- 
## Demo

![shellv0 8 1](https://github.com/user-attachments/assets/3acd94fa-b253-46a7-b362-36c1be5665ca)


## How to Run this Tool in a Windows Machine:
**Requirements:**
- This is a *nix shell and  requires a linux environment e.g. Windows Subsystem of Linux(check [how-to](https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command))  
 - Download the main repo with the green 'code' icon  
 <img width="522" height="437" alt="image" src="https://github.com/user-attachments/assets/8b46cf13-4fa2-4c5d-942c-a6b237c2b550" />

- Extract, inside the extracted folder, mouse click on the path and type 'cmd'
  <img width="570" height="283" alt="image" src="https://github.com/user-attachments/assets/153aff3f-5603-406e-b827-6acdda5f6f00" />  

- Type `wsl -d debian` inside windows cmd, if you have installed `wsl install --distribution debian` like me.  
- **Now that we have a linux envrionment**, test if you  have `python3` , just type it in the terminal.
- If you dont, install python3 with `sudo apt install python3 python3-pip python3-venv -y`. Make sure the system is up-to-date as well: `sudo apt update; sudo apt install libicu-dev pkg-config build-essential`
- **Finally,run `python app/main.py`**. Wait a few second for the dollar $ign to appear.
- If you face error that 'some modules are not installed', then:
	- Create a virtual environment: `python3 -m venv myvenv`. Activate the environment `source ./myvenv/activate`
	- Install some required libraries with `python3 -m pip install -r requirements.txt`. If you face error with this command then make sure that the distinguished python package managers (`setuptools, pip, packaging, wheel`) are up-to-date : ` pip install --upgrade pip setuptools wheel`. Then try again.


## How to attempt this challenge:

**Go to [codecrafters](https://app.codecrafters.io/r/cooperative-sardine-569975)**. Try the current 'free challenge of the month' or buy a subscription.
	
## Walkthrough & Thought-process...
Each "Build your own x" Codecrafters challenge is made of different group of tasks called extensions. 
![alt text](./media/123123.png)

**To implement the pipeline feature** (e.g. `cat /tmp/file | wc -l`) we need to dive into the concept of forks and pipes.

Googling 'python and unix pipes', I get this [empty](https://docs.python.org/3/library/pipes.html) deprecated docs pointing to newer features in [subprocess](https://docs.python.org/3/library/subprocess.html#subprocess.PIPE) module. 

> subprocess.PIPE  
Special value that can be used as the stdin, stdout or stderr argument to Popen and indicates that a pipe to the standard stream should be opened. Most useful with Popen.communicate().

Meaning there are two things we can utilize to implement pipe: `Popen` object constructor and notably `Popen.communicate` method. There are more [methods available ](https://docs.python.org/3/library/subprocess.html#popen-objects).

Popen.communicate(input, timeout) This object method looked very important.
> Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.



```
   import subprocess as s
	cmd = "cat /tmp/file | wc -l"
	pipelist = cmd.split("|")
	p1 = s.Popen(shlex.split(pipelist[0]), stdout=s.PIPE)
	p2 = s.Popen(shlex.split(pipelist[1]), stdin=s.PIPE)
   p2.communicate(p1.stdout.read())....

```
subprocess.run uses Popen underneath. Popen's stout is a io.BufferredRead! so need to use `p1.stdout.read()`. This arrangement works for normal chain commands such as `cat //tmp/ant/file-4 | wc -l` but the following codecrafter test case fails: `tail -f /tmp/owl/file-33 | head -n 5`. Tail with -f flag will not quit on its own and will show newly appended data(that has been appeneded while this command was running!) from the file.
We can pass keyboard stroke ctrl+c also known as signal.SIGINT with this line: `p1.send_signal(signal.SIGINT)` after 1,2 or 3 seconds...
But its not enough to pass the codecrafters test case which will append new data mid-execution. If we use write the code like this:
```

p1 = subprocess.Popen([beforepipe.split()[0], *beforepipe.split()[1:]], stdout=subprocess.PIPE)
p2 = subprocess.Popen([afterpipe.split()[0], *afterpipe.split()[1:]], stdin=subprocess.PIPE)
	try:
		p1.wait(timeout=3)
	except Exception as TimeoutExpired:
		p1.send_signal(signal.SIGINT)
	except:
		sys.stdout.write("command not found, inside runpipe\n")

   p2.communicate(p1.stdout.read()) # this is actually a 'blocking' code, its blocks everything including the debugger! read() seraching for EOF that tail -f is waiting for the user the provide...
```
We get this error:  
![alt text](./media/ss-cf-test-123.png)

If we dont wait() and exit, the p1 command(tail) won't 'catch' the new appended line(that has been appeneded by the user while this command was running.)
After staring at the docs and the wall (and chatgpt), it seems i made the two Popen wrong. I tried to play basketball with two pipes, when i can just 'stitch' them together. `p1.stdout` should be the` stdin` of p2. p1 is tail command and p2 is the head command reading from tail. Now it makes more sense.
```
	p1 = subprocess.Popen([beforepipe.split()[0], *beforepipe.split()[1:]], stdout=subprocess.PIPE)
	p2 = subprocess.Popen([afterpipe.split()[0], *afterpipe.split()[1:]], stdin=p1.stdout)

```

But we still have to figure the waiting and terminating p1 command(`tail`). We can definitely close p1(tail) after p2(head) has finished running as `head -n 5` is supposed to stop and exit after reading 5 lines. Hence: `p2.wait(); p1.terminate()`.

```
	p1.stdout.close() 
   # This close() is general good practise. not particularly relevant to pass the codecrafter test case.
   # The p1.stdout.close() call after starting the p2 is important in order for p1 to receive a SIGPIPE if p2 exits before p1. SIGPIPE is a synchronous signal that’s sent to a process (thread in POSIX.1-2004) which attempts to write data to a socket or pipe that has been closed by the reading end.
   # Hence, after p2(head command) is done printing all lines(`head -n 5), then if p1 attempts to write more, then p1 get SIGPIPE-ed. Though this scenario may or may not happen.
	
   p2.wait()
   # This crucial waiting simply blocks still until p2 exits. If we provide a `timeout=5` argument, then it will throw an exception error (https://alexandra-zaharia.github.io/posts/kill-subprocess-and-its-children-on-timeout-python/#:~:text=The%20timeout%20needs%20to%20be%20specified%20in%20Popen.wait()).

	p1.terminate()
   # Now we can safely quit from the tail command.

	p1.wait()
   # optional cleanup.
```

And this is the final code snippet to pass the task: `Dual-command pipeline #BR6`

```
def runpipes(beforepipe,afterpipe):

	import signal
	p1 = subprocess.Popen([beforepipe.split()[0], *beforepipe.split()[1:]], stdout=subprocess.PIPE)
	p2 = subprocess.Popen([afterpipe.split()[0], *afterpipe.split()[1:]], stdin=p1.stdout)

	p1.stdout.close()
	p2.wait()
	p1.terminate()
	p1.wait()

```
