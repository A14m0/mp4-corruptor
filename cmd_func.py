from importlib import reload
import os
import sys
import random
import global_dat
import atoms as a
import handlers as h

def reload_lib():
    reload(a)
    reload(h)
    a.reload_lib()
    
def _help(args):
    print("""Commands:
    help                prints this help menu
    load <file>         loads file from path <file>
    info                prints the info from currently loaded file
    atoms               prints the atoms of a file
    atom_inf <loc>      prints info about an atom
    corrupt             dialogue for currupting videos :)
    reload              realoads all libraries
    clear               clears the screen
    exit                exits the application""")
    
    return

def _exit(args):
    print("Quitting")
    sys.exit(0)

def clear(args):
    os.system("clear")

def load(args):
    if not os.path.isfile(args):
        print("File %s not found" % args)
        return 1
    else:
        print("Loading file %s" % args)
        f = open(args, "rb")
        global_dat.globdat = f.read()
        f.close()
        print("Length of data: %d" %len(global_dat.globdat))
        a.read_atoms(global_dat.globdat)
        for atom in global_dat.atoms:
            print()
            atom.printMe()
            # if atom.name == "mdat":
            #    print("\tIts an mdat atom. Has no children :)")
            #else:
            a.find_childs(atom)

        print("Load Complete")

def info(args):
    if not global_dat.globdat:
        print("No file loaded")
    else:
        a.get_info()

def _atoms(atom, iterat,  last):
    brkr = "  " + chr(9474)
    brkr = brkr * iterat + "  "
    if last:
       brkr += chr(9492)
    else: 
        brkr += chr(9500)

    brkr += atom.name
    print(brkr)
    
    num = atom.num_children
    i = 0
    for child in atom.children:
        if i == num:
            _atoms(child, iterat+1, True)
        else:
            _atoms(child, iterat+1, False)
        i += 1

def atoms(args):
    print("Atoms: ")
    i = 0
    num = len(global_dat.atoms)
    for atom in global_dat.atoms:
        if i == num:
            _atoms(atom, 0, True)
        else:
            _atoms(atom, 0, False)
            i+=1

def atom_inf(args, q=False):
    atom_arr = args.split("-")
    print(atom_arr)
    if len(atom_arr) == 1:
        for atom in global_dat.atoms:
            if atom.name == atom_arr:
                atom.printMe()
    else:
        for atom in global_dat.atoms:
            if atom.name == atom_arr[0]:
                i = 1
                while i != len(atom_arr):
                    for child in atom.children:
                        if child.name == atom_arr[i]:
                            atom = child
                            i += 1
                            break

                atom.printMe()
               # try:
                func = a.functions.get(atom.name)
                if q:
                    return func(atom.data, True)
                else:
                    return func(atom.data)
                #except Exception as e:
                 #   print("No found handler for atom (exception: %s)" % str(e))
def _find(target, atom):
    ret = None
    if atom.type == 0:
        if atom.name == target:
            ret = atom
    else:
        for child in atom.children:
            if child.name != target:
                ret = _find(target, child)
                if type(ret) != type(None):
                    break
            else:
                ret = child
                break

    return ret

def find(target):
    i = 0
    num = len(global_dat.atoms)
    ret = None
    for atom in global_dat.atoms:
        if target != atom.name:
            ret = _find(target, atom)
            if type(ret) != type(None):
                return ret


def corrupt(args):
    print("Gathering relevant information...")
    sync_samples = 0
    total_offset_entries = 0


    sample_sync = find("stss")
    if type(sample_sync) == type(None):
        print("Could not find audio sync data")
        return
    ss_ret = h.h_stss(sample_sync.data, True)
    sync_samples = ss_ret[0]
    ss_ret = ss_ret[1:]

    tracks = find("co64")
    co_ret = []
    if type(tracks) == type(None):
        tracks = find("stco")
        if type(tracks) == type(None):
            print("Could not find track data")
            return
        co_ret = h.h_stco(tracks.data, True)
    else:
        co_ret = h.h_co64(tracks.data, True)
    total_offset_entries = co_ret[0]
    co_ret = co_ret[1:]
    

    sample_szes = find("stsz")
    if type(sample_szes) == type(None):
        print("Could not find audio sample")
        return
    sz_ret = h.h_stsz(sample_szes.data, True)


    frames = find("stts")
    if type(frames) == type(None):
        print("Could not find frame data")
        return
    ts_ret = h.h_stts(frames.data, True)
    
    print("Corruptable frames: ")

    i = 1
    for frame in ss_ret:
            print("\t [%d] Frame #%d" % (i, frame))
            i += 1
    fram = int(input("Enter a frame # to currupt > "))
    print(len(co_ret))
    print(len(sz_ret)) # sz is wrong... thats for audio samples
    # we should be looking at STSC atom...
    print(sz_ret[0])
    offset = co_ret[fram]
    print("Determined offset %d" % offset)

    print("First 10 bytes at that offset: {}".format(global_dat.globdat[offset:offset+10]))

    i = 1
    for frame in ss_ret:
        if i > fram:
            print("\t [{}] Frame #{}".format(i, frame))
        i += 1

    end_frame=int(input("Enter ending frame >> "))

    print("Corrupting data from frame {} to {}".format(fram, end_frame))
    offset_end = co_ret[end_frame]

    output_data = global_dat.globdat

    first_bit = output_data[:offset]
    corrupt_data = output_data[offset:offset_end]
    last_bit = output_data[offset_end:]

    select = random.randint(0, len(corrupt_data))

    replace_byte = bytes([corrupt_data[select]])
    rand_byte = bytes([random.randint(0, 256)])

    print("Replacing {} with {}".format(replace_byte, rand_byte))
    out_data = corrupt_data.replace(replace_byte, rand_byte)

    f = open("Output.mp4", "wb")
    tot_written = f.write(first_bit)
    tot_written += f.write(out_data)
    tot_written += f.write(last_bit)
    f.close()

    print("Wrote data to file ({} bytes, len of corrupt: {})".format(tot_written, len(corrupt_data)))
