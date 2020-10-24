# coding:utf8
import hashlib
import string
import sys
import urllib.request
import urllib.response
import urllib.error
from utils import *


def crack_dict(md5, file):
    """
        Break an MD5 HASH (md5) via a list of keywords (file)
        :param md5: Hash MD5 TO BREAK
        :param file: Keyword file to use
        :return:
        """
    try:
        find = False
        ofile = open(file, "r")
        for word in ofile.readlines():
            word = word.strip("\n")
            hashmd5 = hashlib.md5(word.encode("utf8")).hexdigest()
            if hashmd5 == md5:
                print(Color.GREEN + "[+] Password found : " + str(word) + " (" + hashmd5 + ")" + Color.END)
                find = True
        if not find:
            print(Color.RED + "[-] Password not found :(" + Color.END)
        ofile.close()
    except FileNotFoundError:
        print(Color.RED + "[-] Error: folder name or file not found !" + Color.END)
        sys.exit(1)
    except Exception as err:
        print("Color.RED + [-] Error : " + str(err) + Color.END)
        sys.exit(2)


def crack_incr(md5, length, currpass=[]):
    """
    Break an MD5 HASH via an incremental method for a mdp of length length
    :param md5: The md5 hash to break
    :param length: The length of the password to find
    :param currpass: temporary list automatically used via recursion containing the current mdp test
    :return:
    """

    letters = string.printable
    if length >= 1:
        if len(currpass) == 0:
            currpass = ['a' for _ in range(length)]
            crack_incr(md5, length, currpass)
        else:
            for c in letters:
                currpass[length - 1] = c
                currhash = hashlib.md5("".join(currpass).encode("utf8")).hexdigest()
                print("[*] TEST TO : " + "".join(currpass) + " (" + currhash + ")")
                if currhash == md5:
                    print(Color.GREEN + "[+] Password found : " + "".join(currpass) + Color.END)
                    sys.exit(0)
                else:
                    crack_incr(md5, length - 1, currpass)


def crack_en_ligne(md5):
    """
    Search for an MD5 HASH via google.fr
    :param:md5 md5 hash to use for online search
    :return:
    """

    try:
        agent_user = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
        headers = {'User-Agent': agent_user}
        url = "https://www.google.fr/search?hl=fr&q=" + md5
        requete = urllib.request.Request(url, None, headers)
        reponse = urllib.request.urlopen(requete)
    except urllib.error.HTTPError as e:
        print(Color.RED + "[-] Error HTTP : " + e.code + Color.END)
    except urllib.error.URLError as e:
        print(Color.RED + "[-] Error d'URL : " + e.reason + Color.END)

    if "NO DOCUMENT" in reponse.read().decode("utf8"):
        print(Color.RED + "[-] HASH NOT FOUND WITH GOOGLE" + Color.END)
    else:
        print(Color.GREEN + "[+] PASSWORD FOUND WITH GOOGLE : " + url + Color.END)