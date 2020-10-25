#!/usr/bin/env python3
# coding:utf-8
import time
import argparse
import atexit
from cracker import *
import multiprocessing


def duration_poster():
    """
    Shows the duration of the program
    :return:
    """

    print("Elapsed time : " + str(time.time() - start) + " seconds")


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

    work_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()
    cracker = Cracker()
    start = time.time()
    atexit.register(duration_poster)

    if args.gen:
        print("[*] HASH MD5 TO " + args.gen + " = " + hashlib.md5(args.gen.encode("utf8")).hexdigest())

    if args.md5:
        print("[*] HASH CRACKING " + args.md5)
        if args.file:
            print("[*] USING THE KEYWORDS FILE " + args.file)

            p1 = multiprocessing.Process(target=Cracker.work, args=(work_queue, done_queue, args.md5, args.file,
                                                                    Order.DESCEND))
            work_queue.put(cracker)
            p1.start()

            p2 = multiprocessing.Process(target=Cracker.work, args=(work_queue, done_queue, args.md5, args.file,
                                                                    Order.ASCEND))
            work_queue.put(cracker)
            p2.start()

            while True:
                data = done_queue.get()

                if data == "FIND" or data == "NOT FOUND":
                    p1.kill()
                    p2.kill()
                    break

        elif args.plength:
            print("[*] USING INCREMENTAL MODE TO " + str(args.plength) + " LETTER(S)")
            Cracker.crack_incr(args.md5, args.plength)
        elif args.online:
            print("[*] USING ONLINE MODE")
            Cracker.crack_online(args.md5)
        else:
            print(Color.RED + "[-] PLEASE CHOOSE THE ARGUMENT -f OR -l with -md5." + Color.END)
    else:
        print(Color.RED + "[-] HASH MD5 NOT PROVIDED." + Color.END)
