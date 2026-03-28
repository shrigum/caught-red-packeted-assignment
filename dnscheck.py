import base64, re

# read data
f = open('dnssummary.csv')
lines = f.readlines()
f.close()

# extract and save each file data
# we know there are 2 files from chunk numbers 1.x / 2.x
# some chunks are duplicated, but all seem in order so we just need to dedupe
for file_id in [1, 2]:
    prefix = "TXT " + str(file_id) + "."
    recovered_data = ""

    seen = set()
    for line in lines:
        if prefix not in line:
            continue
        part = line.split(prefix)[1]
        chunk_num = int(part.split(".")[0])
        if chunk_num in seen:
            continue
        seen.add(chunk_num)
        data = part.split(".")[1]
        data = data.split(".verysecret")[0]
        recovered_data += data

    raw = base64.b64decode(recovered_data)

    # first file just has text, second file starts with '/9j/'
    ext = {1: ".txt", 2: ".jpg"}
    f = open("recovered_file_" + str(file_id) + ext[file_id], "wb")
    f.write(raw)
    f.close()
