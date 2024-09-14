from zlib import crc32

data = bytearray(open("finish.png",'rb').read())

# go through each chunk
# replace the current crc32 with the correct one
# loop until it reaches the end of the file

# skip PNG file signature ('89 50 4E 47 0D 0A 1A 0A')
i = 8

while True:
    try:
        chunk_size = int(data[i:i+4].hex(), 16)
        i += 4

        chunk_header = data[i:i+4]
        i += 4

        chunk_data = data[i:i+chunk_size]
        i = i+chunk_size

        chunk_crc = data[i:i+4]

        real_crc = hex(crc32(chunk_header+chunk_data))[2:].zfill(8)

        # update the crc's
        data[i:i+4] = bytes.fromhex(real_crc)
        i += 4

    except:
        break

# write the modified data into a new file
new = open("finish_fixed.png", "wb")
new.write(data)