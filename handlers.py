import struct

def h_stts(data, q=False):
    duration = 0
    offset = 8
    for i in range(int(len(data[8:])/8)):
        duration += struct.unpack(">I", data[offset:offset+4])[0]
        delta = struct.unpack(">I", data[offset+4:offset+8])
        offset += 8

    if not q:
        print("Number of frames: %d" % duration)
    return duration

def h_stsz(data, q=False):
    vf = struct.unpack(">I", data[8:12])[0]
    v = vf >> 3
    
    if not q:
        print("Version: %d" % v)
        print("Flags: %d" % vf)

    unif_sz = struct.unpack(">I", data[12:16])[0]

    if not q:
        print("Uniform size of samples (ignore if 0): %d" % unif_sz)
    tot_entries = struct.unpack(">I", data[16:20])[0]
    
    if not q:
        print("Total number of samples: %d" % tot_entries)

    ret = []

    if unif_sz == 0:
        offset = 20
        for i in range(tot_entries):
            entry = struct.unpack(">I", data[offset:offset+4])[0]
            ret.append(entry)
            if not q:
                print("Sample %d has size %d" % (i, entry))
            offset += 4
    
    
    return ret

def h_trak(data):
    return

def h_mvhd(data):
    return

def h_tkhd(data):
    return

def h_mdia(data):
    return

def h_minf(data):
    return

def h_hdlr(data):
    vers = struct.unpack(">I", data[8:12])[0]
    flags = struct.unpack(">I", data[12:16])[0]
    comp_name = b"".join(struct.unpack(">cccc", data[16:20])).decode()
    subtype = struct.unpack(">I", data[20:24])[0]
    manu = struct.unpack(">I", data[24:28])[0]
    flags = struct.unpack(">I", data[28:32])[0]
    tmp = "c" * (len(data)-32)
    formt = ">" + tmp
    name = b"".join(struct.unpack(formt, data[32:])).decode()
    print("Component type: %s" % comp_name)
    print("Name: %s" % name)
    return

def h_mdhd(data):
    vf = struct.unpack(">I", data[8:12])[0]
    v = vf >> 3
    if (v == 0):
        creat = struct.unpack(">I", data[12:16])[0]
        modif = struct.unpack(">I", data[16:20])[0]
        tim = struct.unpack(">I", data[20:24])[0]
        dur = struct.unpack(">I", data[24:28])[0]
        lang = struct.unpack(">H", data[28:30])[0]
        qual = struct.unpack(">H", data[26:28])[0]
    else:
        creat = struct.unpack(">Q", data[12:20])[0]
        modif = struct.unpack(">I", data[20:28])[0]
        tim = struct.unpack(">I", data[28:32])[0]
        dur = struct.unpack(">I", data[32:40])[0]
        lang = struct.unpack(">H", data[40:42])[0]
        qual = struct.unpack(">H", data[42:44])[0]

    print("Version: %d" % v)
    print("Flags: %d" % vf)
    print("Creation time: %d" % creat)
    print("Modification time: %d" % modif)
    print("Time scale: %d" % tim)
    print("Duration: %d" % dur)
    print("Language: %hu" % lang)
    print("Quality: %hu" % qual)

    print("Play time: %.2f minutes" % ((dur/tim)/60.0))
    return

def h_dinf(data):
    return

def h_stbl(data):
    return

def h_dref(data):
    return

def h_stco(data, q=False):
    vf = struct.unpack(">I", data[8:12])[0]
    v = vf >> 3
    
    if not q:
        print("Version: %d" % v)
        print("Flags: %d" % vf)
    
    tot_entries = struct.unpack(">I", data[12:16])[0]
    
    if not q:
        print("Total chunk entries: %d" % tot_entries)
    offset = 16
    
    ret = []
    ret.append(tot_entries)
    for i in range(tot_entries):
        entry = struct.unpack(">I", data[offset:offset+4])[0]
        ret.append(entry)
        if not q:
            print("Offset @ offset %d" % entry)
        offset += 4
    
    return ret

def h_stss(data, q=False):
    vf = struct.unpack(">I", data[8:12])[0]
    v = vf >> 3
    
    if not q:
        print("Version: %d" % v)
        print("Flags: %d" % vf)

    tot_entries = struct.unpack(">I", data[12:16])[0]
    
    if not q:
        print("Total number of sync samples: %d" % tot_entries)

    ret = []
    ret.append(tot_entries)
    offset = 16
    for i in range(tot_entries):
        entry = struct.unpack(">I", data[offset:offset+4])[0]
        ret.append(entry)
        if not q:
            print("Sync sample @ frame %d" % entry)
        offset += 4
    
    return ret

def h_vmhd(data):
    return

def h_co64(data, q=False):
    vf = struct.unpack(">I", data[8:12])[0]
    v = vf >> 3
    
    if not q:
        print("Version: %d" % v)
        print("Flags: %d" % vf)

    tot_entries = struct.unpack(">I", data[12:16])[0]
    ret = []
    ret.append(tot_entries)

    if not q:
        print("Total chunk entries: %d" % tot_entries)
    
    offset = 16
    for i in range(tot_entries):
        entry = struct.unpack(">Q", data[offset:offset+8])[0]
        ret.append(entry)
        
        if not q:
            print("Offset @ offset %d" % entry)
        offset += 8
    
    return ret

def h_stsc(data, q=False):
    return