# coding:utf-8
import hashlib
import string
import sys
import urllib.request
import urllib.response
import urllib.error
from utils import *


class Cracker:
    @staticmethod
    def crack_dict(md5, file, order, done_queue):
        """
        Break an MD5 HASH (md5) via a list of keywords (file)
        :param done_queue:
        :param order:
        :param md5: Hash MD5 to break
        :param file: Keyword file to use
        :return:
        """

        try:
            find = False
            ofile = open(file, "r")
            if Order.ASCEND == order:
                content = reversed(list(ofile.readlines()))
            else:
                content = ofile.readlines()
            for word in content:
                word = word.strip("\n")
                hashmd5 = hashlib.md5(word.encode("utf8")).hexdigest()
                if hashmd5 == md5:
                    find = True
                    print(Color.GREEN + "[+] PASSWORD FOUND : " + word + " (" + hashmd5 + ")" + Color.END)
                    done_queue.put("FIND")
                    break
            if not find:
                print(Color.RED + "[-] PASSWORD NOT FOUND :(" + Color.END)
                done_queue.put("NOT FOUND")
            ofile.close()
        except FileNotFoundError:
            print(Color.RED + "[-] ERROR: folder or file name not found !" + Color.END)
            sys.exit(1)
        except Exception as err:
            print(Color.RED + "[-] ERROR : " + str(err) + Color.END)
            sys.exit(2)

    @staticmethod
    def crack_incr(md5, length, _currpass=[]):
        """
        Break an MD5 HASH via an incremental method for a mdp of length length
        :param md5: The md5 hash to break
        :param length: The length of the password to ENDd
        :param _currpass: temporary list automatically used via recursion containing the current mdp test
        :return:
        """

        letters = string.printable

        if length >= 1:
            if len(_currpass) == 0:
                _currpass = ['a' for _ in range(length)]
                Cracker.crack_incr(md5, length, _currpass)
            else:
                for c in letters:
                    _currpass[length - 1] = c
                    currhash = hashlib.md5("".join(_currpass).encode("utf8")).hexdigest()
                    print("[*] TEST OF : " + "".join(_currpass) + " (" + currhash + ")")
                    if currhash == md5:
                        print(Color.GREEN + "[+] PASSWORD FOUND : " + "".join(_currpass) + Color.END)
                        sys.exit(0)
                    else:
                        Cracker.crack_incr(md5, length - 1, _currpass)
        else:
            return

    @staticmethod
    def crack_online(md5):
        """
        Search for an MD5 HASH via google.fr
        :param:md5 md5 hash to use for online search
        :return:
        """

        try:
            user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
            headers = {'User-Agent': user_agent}
            url = "https://www.google.fr/search?hl=fr&q=" + md5
            requete = urllib.request.Request(url, None, headers)
            reponse = urllib.request.urlopen(requete)
        except urllib.error.HTTPError as e:
            print(Color.RED + "[-] ERROR HTTP : " + e.code + Color.END)
        except urllib.error.URLError as e:
            print(Color.RED + "[-] ERROR d'URL : " + e.reason + Color.END)

        if "No document" in reponse.read().decode("utf8"):
            print(Color.RED + "[-] HASH NOT FOUND VIA GOOGLE" + Color.END)
        else:
            print(Color.GREEN + "[+] PASSWORD FOUND VIA GOOGLE : " + url + Color.END)

    @staticmethod
    def work(work_queue, done_queue, md5, file, order):
        """

        :param work_queue:
        :param done_queue:
        :param md5:
        :param file:
        :param order:
        :return:
        """
        o = work_queue.get()
        o.crack_dict(md5, file, order, done_queue)
