from time import asctime

__logfile = "./log/logs.log"

def write(msg):
    with open(__logfile, "a+") as fp:
        print(msg)
        fp.write(msg + "\t" + asctime() + "\n")
