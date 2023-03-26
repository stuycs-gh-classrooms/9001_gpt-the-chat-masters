from parser import parse_script

filename = "script"

with open(filename, "r") as f:
    script = f.readlines()

parse_script(script)
