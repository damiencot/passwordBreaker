#!/usr/bin/env python3
# coding:utf8
import time
import argparse
import atexit
from cracker import *


def affiche_duree():
    """
    Shows the duration of the program
    :return:
    """

    print("Elapsed time: " + str(time.time() - debut) + " secondes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python password breaker")
    parser.add_argument("-f", "--file", dest="file", help="Keyword file path", required=False)
    parser.add_argument("-g", "--gen", dest="gen", help="Generate an MD5 hash of the given password", required=False)
    parser.add_argument("-md5", dest="md5", help="MD5 password to break", required=False)
    parser.add_argument("-l", dest="plength", help="Password length (incremental mode only)",
                        required=False, type=int)
    parser.add_argument("-o", dest="online", help="Search the hash online (google)", required=False,
                        action="store_true")

    args = parser.parse_args()

    debut = time.time()
    atexit.register(affiche_duree)

    if args.gen:
        print("[*] HAHS MD5 DE " + args.gen + " : " + hashlib.md5(args.gen.encode("utf8")).hexdigest())

    if args.md5:
        print("[*] CRACKING DU HASH " + args.md5)
        if args.file:
            print("[*] USING THE KEYWORDS FILE " + args.file)
            crack_dict(args.md5, args.file)
        elif args.plength:
            print("[*] USING INCREMENTAL MODE TO " + str(args.plength) + " LETTER(S)")
            crack_incr(args.md5, args.plength)
        elif args.online:
            print("[*] USING ONLINE MODE")
            crack_en_ligne(args.md5)
        else:
            print(Color.RED + "[-] PLEASE CHOOSE THE ARGUMENT -f or -l with -md5." + Color.END)
    else:
        print(Color.RED + "[-] HASH MD5 NOT PROVIDED." + Color.END)