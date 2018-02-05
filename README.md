# Duplicates
Duplicates program finds duplicate files or directories in the given directory by using recursive way.
## PROBLEM DESCRIPTION
	In this project, the duplicates program must find the duplicates files or directories in given directories
  or current directory if the part of directory is empty.This is the main problem of this program but it has
  some other prominent parts such as parsing command, finding pattern and pattern matching clearly. This duplicates
  program must find duplicate directories or files with recursive way like hash trees by considering arguments
  in command line. In addition, parsing the command working for program in shell is the other problem of this project.
  Different arguments can come in command to do different missions like printing, executing given command for duplicates.
  For example, if -c comes, the command coming from -c must be worked for duplicates in the terminal and returned output.
  Otherwise, the program prints duplicate directories or files according to arguments in input that whether includes -d
  for directory or not. Moreover, pattern part is related to regular expression and the problem of matching with given
  pattern precisely. Pattern must be selected from list containing directories and pattern clearly and the duplicates
  program should accept only the duplicate pairs with matching with pattern and pattern must be searched in the last
  portion of directories which is the name of the file or the last name of directory. In essence, the duplicates program
  must find the duplicate files or directories according to input arguments and apply some duties again according to given
  arguments. After that, pattern should be taken account of if it is given and duplicate results must be considered in the
  case of matching with it precisely. 
  
 ## PROBLEM SOLUTION
	In order to create this program finding duplicates exactly, I need an useful and convenient parser which can parse the
  command line clearly and constitute different missions by evaluating the arguments. Therefore, I have to choose the best
  parser for this aims so that I chose argparse() library because I can arrange my actions by considering arguments properly.
  I parse my command line input by evaluating different options in the description and I obtain enough knowledge about parsing.
  
  Also, I left the remaining part as the combination of pattern and directories. Hence, I create a list containing this
  remaining part and divide the argument parts after using them. Then, I parse this remaining list to find the pattern in it.
  I access the list including merely directories after pattern is vanished from list. Thus, I handle the parsing part and come
  finding duplicate part. 
  
  I start to traverse directories by considering the information coming from arguments and the directories and files is
  traversed differently. For files, it is easier than directories because I traverse directories in given ones and I store
  it if the directory represents file. For directories, I write recursive method that finds its own hash value by concatenating
  the sorted hash list. Their hash values is also saved in global dictionary. 
  
  After I find duplicates files or directories, searching pattern in duplicates is coming. I want not to print or work
  with command ones that are not available for regex so that I search the dictionary and find the indexes of duplicates
  which are not true. In addition, I erase these duplicates from dictionary and obtain necessary one. Then, I evaluate 
  if command line input includes -c for command or not. If it does not have -c, then printing part comes. For this, I only
  traverse dictionary as sorted lists including duplicates. I print the list of duplicates which passes the test of pattern
  matching.
