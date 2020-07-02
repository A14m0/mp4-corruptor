import struct
import global_dat
from importlib import reload
from binascii import hexlify
import handlers as h


functions = {"stts":h.h_stts,
            "stsz":h.h_stsz,
            "trak":h.h_trak,
            "mvhd":h.h_mvhd,
            "tkhd":h.h_tkhd,
            "mdia":h.h_mdia,
            "minf":h.h_minf,
            "hdlr":h.h_hdlr,
            "mdhd":h.h_mdhd,
            "dinf":h.h_dinf,
            "stbl":h.h_stbl,
            "dref":h.h_dref,
            "stco":h.h_stco,
            "stss":h.h_stss,
            "vmhd":h.h_vmhd,
            "co64":h.h_co64,
            }

def reload_lib():
    reload(h)

class Atom:
    def __init__(self, size, name, data, typ=1):
        self.size = size
        self.name = name
        self.data = data
        self.children = []
        self.num_children = 0
        self.type = typ

    def printMe(self):
        print("Atom %s size: %d" % (self.name, self.size))
       
def find_childs(child):
    if not child.type:
        print("Data atom. No children")
        return
    i = 8
    
    print("Child data for %s" % child.name)

    while i < child.size:
        typ = 1
        siz = struct.unpack(">I", child.data[i:4+i])[0]
        if siz > child.size or siz == 0:
            print("\tData atom")
            typ = 0
            break
        else:
            dat = child.data[i:i+siz]

            nam_tup = struct.unpack(">cccc", child.data[i+4:i+8])
            try:
                nam = b"".join(nam_tup).decode()
            except UnicodeDecodeError:
                print("\t\tName cannot be decoded (probs a funky data atom)")
                nam = ""
            print("\tChild atom %s (size: %d)" % (nam, siz))
            child.children.append(Atom(siz, nam, dat, typ))
            child.num_children += 1
            #print("\tadded atom to array. total: %d" % child.num_children)
        i += siz
    
    print()
    for chld in child.children:
        find_childs(chld)

def read_atoms(data):
    if len(data) > 0:
        siz = struct.unpack(">I", data[:4])[0]
        print("size: %d" % siz)
        nam_tup = struct.unpack(">cccc", data[4:8])
        nam = b"".join(nam_tup).decode()
        global_dat.atoms.append(Atom(siz, nam, data))
        print("added atom to array. total: %d" % len(global_dat.atoms))
        read_atoms(data[siz:])

def find(atom, target):
    for child in atom.children:
        if child.name == target:
            return child
    return None

def get_info():
    #moov->trak->mdia->dhd
    for atom in global_dat.atoms:
        if atom.name == "moov":
            trak = find(atom, "trak")
            if trak:
                mdia = find(trak, "mdia")
                if mdia:
                    mdhd = find(mdia, "mdhd")
                    if mdhd:
                        h.h_mdhd(mdhd.data)
    
    return