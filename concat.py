#!/usr/bin/env python
# coding:utf-8

# require ffmpeg version 1.1 or higher

import dircache, os, shlex, sys
from subprocess import Popen, PIPE, STDOUT

class MovieManager:

    list_file_name = "mylist.txt"
    support_ext_list = [".mp4", ".flv", ".avi"]
    target_ext = None
    output = None

    def __init__(self):
        self.target_ext = self._guess_ext()
        self.output = "output" + self.target_ext

    def concat_movie(self):
        self._generate_list_file()
        cmd = ("ffmpeg -y -f concat -i " + self.list_file_name
               + " -c copy output" + self.target_ext)
        p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, shell=False)
        stdout_data, stderr_data = p.communicate()
        print("stdout : %s, stderr : %s" % (stderr_data, stderr_data))
        self._remove_list_file()
        print("complete!!")

    def _remove_list_file(self):
        try:
            os.remove(self.list_file_name)
        except OSError, e:
            print(e)

    def _generate_list_file(self):
        if self.target_ext not in self.support_ext_list:
            print("%s doesn't support. exit." % self.target_ext)
            sys.exit(1)
        try:
            with open(self.list_file_name, "w") as fp:
                for file in dircache.listdir("./"):
                    if (os.path.splitext(file)[1] == self.target_ext
                            and file != self.output):
                        buf = "file '" + file + "'\n"
                        fp.write(buf)
        except IOError, e:
            print(e)

    def _guess_ext(self):
        return_ext = None
        list = dircache.listdir("./")
        for file in list:
            file_ext = os.path.splitext(file)[1]
            if file_ext in self.support_ext_list:
                return_ext = file_ext
                break
        return return_ext
                            
if __name__ == '__main__':
    movieManager = MovieManager()
    movieManager.concat_movie()
