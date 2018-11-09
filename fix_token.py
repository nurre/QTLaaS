def fix_token_file():
    filename = "token.txt"
    f = open(filename,"r")
    lines = f.readlines()
    token = ""
    for line in lines:
        if "?token=" not in line:
            continue
        i = line.find("?token=")
        token = line[i + len("?token="):].split()[0]+"\n"
        break
    f = open(filename, "w")
    f.write(token)
    f.close()

