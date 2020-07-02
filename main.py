#!/usr/bin/env python3

import struct
from importlib import reload
import handlers
import atoms 
import cmd_func
import global_dat


def reload_all(args):
    print("Reloading all libraries")
    try:
        reload(cmd_func)
        cmd_func.reload_lib()
        reload(global_dat)
        print("Done")
    except Exception as e:
        print("Failed to reload libraries: ")
        print(str(e))


commands = {"help": cmd_func._help,
            "exit": cmd_func._exit,
            "clear": cmd_func.clear,
            "load": cmd_func.load,
            "info": cmd_func.info,
            "atoms": cmd_func.atoms,
            "reload": reload_all,
            "atom_inf": cmd_func.atom_inf,
            "corrupt": cmd_func.corrupt,
            }

def main():
    global_dat.init()
    cmd = ""
    while 1:
        cmd = input(" > ").split(" ")
        if not cmd[0] in commands:
            print("Unknown command %s (type \"help\" for more)" % cmd[0])
        else:
            commands.get(cmd[0])(" ".join(cmd[1:]))

if __name__ == "__main__":
    main()
        
# https://wiki.multimedia.cx/index.php/QuickTime_container#mdia
# http://atomicparsley.sourceforge.net/mpeg-4files.html