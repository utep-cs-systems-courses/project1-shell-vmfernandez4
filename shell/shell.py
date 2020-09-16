import sys, os, re

def handle_input(command):
    user_args = command.split()
    if command == "": #User input
        pass
    elif 'exit' in command: # Exits
        sys.exit(0)
    elif 'cd' in user_args[0]:
        try:
            if len (user_args) >= 2: # Changes directory
                os.chdir(user_args[1])
            else: # Goes back one directory(cd .._)
                os.chdir("..")
        except FileNotFoundError:
            os.write(1,("cd %s: No directory found" % user_args[1]).encode())
            pass
    elif '|' in user_args:
        print()

def prompt():
    while True:
        if 'PS1' in os.environ:
            os.write(1,(os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())
        try:
            command = input()
        except ValueError:
            sys.exit(1)
        handleInput(command)

def execute(user_args):
    rc = os.fork()
    pid = os.get_pid()
    
    if rc == 0:
        for dir in re.split(":", os.environ['PATH']): 
            launch = "%s/%s" % (dir, user_args[0])
            try:
                os.execve(launch, user_args, os.environ)
            except FileNotFoundError:
                pass
        os.write(2,("%s: Command not found\n" % user_args[0]).encode())

    elif rc < 0:
        os.write(2,("Unsuccessful fork%d\n" %rc).encode())
        sys.exit(1)

    else:
        child_pid = os.wait()

if __name__ == "__main__":
    prompt()