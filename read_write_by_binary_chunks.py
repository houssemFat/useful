# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import os
MAX_CHUNK_SIZE = 1024 # 1k
def copy (target_name, data, chunk_size, chunk_index, last_chunk):
    seek_start = chunk_size * chunk_index
    print len (data)
    #print seek_start
    with open(target_name, 'ab') as f :
        f.seek (0, seek_start)
        f.write(data)
        f.close ()

def read_and_copy (filename, target_name):
    chunk_index = 0
    last_chunk = False
    print filename
    # must use rb !
    with open(filename, "rb") as file :
        file.seek(0)
        while (not last_chunk):
            data = file.read (MAX_CHUNK_SIZE)
            #print chunk_index
            if len(data) == 0 :
                last_chunk = True
            copy (target_name, data, MAX_CHUNK_SIZE, chunk_index, last_chunk)
            chunk_index = chunk_index + 1
        file.close()
    print chunk_index



if __name__ == "__main__":
    length = len(sys.argv)
    if length < 2:
        raise Exception("Error no filename specified !")
    filename = sys.argv [1]
    target_name = filename + '_2'
    if os.path.isfile(target_name):
        response = raw_input("file %s already exists, would you like to override current file (y/yes): " % target_name)
        if (response == 'y' or response == 'yes'):
            os.remove(target_name)
            read_and_copy(filename, target_name)
    else :
        read_and_copy(filename, target_name)
