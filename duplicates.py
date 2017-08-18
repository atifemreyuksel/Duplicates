import re
import os
import pwd
import sys
import subprocess
import hashlib
import argparse
import collections

dictionary = {}                                                                                      #This is the hash dictionary that stores the duplicates.

def find_hash_value(direc):                                                                          #This method finds the hash value of the string regarding sha256.
    hash_object = hashlib.sha256(direc)                                                              #Hashlib converts the string to hash object.
    hex_dig = hash_object.hexdigest()                                                                #Hexdigest method converts hash object to hash value.
    return hex_dig

def recursive_hash_directory(directory, contaim, dictionary):                                        #Finds duplicates directories by doing recursively and helps dictionary.
    fullpathname = directory.pop()
    curlist = os.listdir(fullpathname)                                                               #Curlist includes the contents of the below paths of main path.
    while curlist:
        name_of_file = curlist.pop()
        newpath = fullpathname + "/" + name_of_file                                                  #Newpaths are become absolute path by adding fullpathname to name of file or directory.
        if os.path.isfile(newpath):
            if name_of_file != ".DS_Store":                                                          #This is the exception handling for MACOS system.
                cont = open(newpath).read()
                cont2 = find_hash_value(cont)
                contaim.append(cont2)

        if os.path.isdir(newpath):
            contaim.append(find_hash_value(recursive_hash_directory([newpath], [], dictionary)))     #If main directory contains new directories in curlist, then we send
                                                                                                     # it to recursion and we append its result to the hash list of main path list.
    contaim.sort()                                                                                   #List containing hash value of directory is sorted to control easily.
    stri = ""
    for i in range(0, len(contaim)):
        stri = stri + contaim[i]
    cont2 = find_hash_value(stri)
    if cont2 in dictionary:
        dictionary[cont2].append(fullpathname)
    else:
        dictionary[cont2] = [fullpathname]                                                           #Hash value stores to dictionary with the key that is full path name.
    return find_hash_value(stri)

class duplicates:                                                                                      #This class is the main program.

    def duplicate(self):                                                                                  #This is the main method of the program or class.
        parser = argparse.ArgumentParser()                                                           #Parser with argparse facilitates the problem of parsing.
        parser.add_argument('-p', action='store_true')                                               #Parser with argument -p controls whether or not command line includes -p.
        parser.add_argument('-d', action='store_true')                                               #Parser with argument -d controls whether or not command line includes -d.
        parser.add_argument('-f', action='store_true')                                               #Parser with argument -f controls whether or not command line includes -f.
        parser.add_argument('-c', nargs=1)                                                           #Parser with argument -c takes the argument that is next to -c and stores it.
        parser.add_argument('remain', nargs=argparse.REMAINDER)                                      #Parser that defined as remain constitutes list from the remainder part involving pattern and directories.
        pars=parser.parse_args()                                                                     #This is the object of parser.

        remaining = pars.remain
        pattern = ".*"                                                                               #This pattern is initialized like that since if input does not have pattern, this regex works with every string.
        control2 = False                                                                             #This is the boolean for controlling the existence of pattern.
        indix = 0
        for a in range(0, len(remaining)):
            if remaining[a].startswith("\'") or remaining[a].startswith("\""):                       #This statement controls if element of list overlaps with pattern or not.
                control2 = True
                pattern = remaining[a][1:-1]
                indix = a
        if control2:
            del remaining[indix]

        if len(remaining) == 0:
            remaining.append(os.getcwd())                                                            #If there is not directory in input, then current directory is added to list.

        direclists = []                                                                              #Stores the files in it in the else part and divides directory and list.
        if pars.d:
            for i in range(0, len(remaining)):
                astring = remaining[i]
                dirlist = [remaining[i]]
                if not os.path.isdir(astring):
                    dirlist = [os.getcwd() + "/" + remaining[i]]                                     #If an element consists of merely the last portion of the directory, then current directory is added to its beginning.
                string = recursive_hash_directory(dirlist, [], dictionary)                           #This is the recursive directory step.

        else:                                                                                        #Statement is created for finding duplicate files.
            for i in range(0, len(remaining)):
                astring = remaining[i]
                dirlist = [remaining[i]]
                if not os.path.isdir(astring):
                    dirlist = [os.getcwd() + "/" + remaining[i]]

                while dirlist:                                                                       #This is another traversing directory loop like recursion.
                    fullpathname = dirlist.pop()
                    curlist = os.listdir(fullpathname)
                    for fdname in curlist:
                        newpath = fullpathname + "/" + fdname
                        if os.path.isfile(newpath):
                            direclists.append(newpath)
                        if os.path.isdir(newpath):
                            dirlist.append(newpath)                                                  #If there is extra directory, it is also added to traverse.

            for a in range(0, len(direclists)):
                if os.path.isfile(direclists[a]):
                    cont = open(direclists[a]).read()
                    cont2 = find_hash_value(cont)
                    if cont2 in dictionary:
                        dictionary[cont2].append(direclists[a])                                      #Hash value of files is made as pair and added to dictionary.
                    else:
                        dictionary[cont2] = [direclists[a]]

        listof = []                                                                                  #Stores lists that keep indexes of element in the dictionary not to be available to regular expression.
        for key1 in dictionary:                                                                      #This loop searches which duplicates cannot pass the test of regular expression.
            dictionary[key1].sort()
            if len(dictionary[key1]) > 1:
                count = 0
                lists = [key1]
                for i in range(0, len(dictionary[key1])):
                    if not re.search(pattern, os.path.basename(os.path.normpath(dictionary[key1][i])), flags=0):   #This statement searches for pattern in the last portion of directory of duplicates.
                        lists.append(i-count)
                        count += 1                                                                   #I use count not to be faced with the problem of list out of range.
                listof.append(lists)
        for i in range(0, len(listof)):
            if len(listof[i]) > 1:
                for j in range(1, len(listof[i])):
                    del dictionary[listof[i][0]][listof[i][j]]                                       #T erase not useful duplicates according to regular expression.

        if pars.c:                                                                                   #If command line input includes -c, this statement works to process command.
            command = pars.c[0]
            for key in dictionary:
                if len(dictionary[key]) > 1:
                    for i in range(0, len(dictionary[key])):
                        cmd = command + " " + dictionary[key][i]
                        os.system(cmd)                                                               #cmd is executed and returns output by using os.system.
        else:
            for key2 in dictionary:
                if len(dictionary[key2]) > 1:
                    for i in range(0, len(dictionary[key2])):
                        print dictionary[key2][i],                                                   #Prints directories side by side that are duplicates one.
                    print ''

duplicates().duplicate()
