import getpass
import os
import argparse
import sys

user = getpass.getuser()

afs_path = "/home/{0}/afs".format(user)
execute_path = os.path.dirname(os.path.realpath(sys.argv[0]))

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--uninstall", help="uninstall", action="store_true")
parser.add_argument("-a", "--afs", help="execute in HOME/afs", action="store_true")
parser.add_argument("-p", "--path", help="select path")
args = parser.parse_args()


def modify_file_good(T):
    for i in range(len(T)):
        T[i] = T[i].replace(";", ";")
        T[i] = T[i].replace("і", "i")


def modify_file_bad(T):
    for i in range(len(T)):
        T[i] = T[i].replace(";", ";")
        T[i] = T[i].replace("i", "і")


def files_scanning(path, func):
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            entry_path = path + "/" + entry.name
            if entry.is_dir():
                files_scanning(entry_path, func)
            else:
                if entry.name.split('.')[-1] == "cs":
                    print("modifying: " + entry_path)
                    with open(entry_path, "r") as file:
                        text = file.readlines()
                        func(text)
                    with open(entry_path, "w") as file:
                        file.writelines(text)


if args.uninstall:
    func = modify_file_good
else:
    func = modify_file_bad

if args.afs:
    files_scanning(afs_path, func)
elif args.path:
    files_scanning(args.path, func)
else:
    files_scanning(execute_path, func)
