#FILE HANDLING
#"r" - Read - Default value. Opens a file for reading, error if the file does not exist
#"a" - Append - Opens a file for appending, creates the file if it does not exist
#"w" - Write - Opens a file for writing, creates the file if it does not exist
#"x" - Create - Creates the specified file, returns an error if the file exists

#"t" - Text - Default value. Text mode
#"b" - Binary - Binary mode (e.g. images)

f = open("demofile.txt")

f = open("demofile.txt", "rt")

#Hello! Welcome to demofile.txt.  This file is for testing purposes. Good Luck!

f = open("demofile.txt", "r")
print(f.read())

f = open("D:\\myfiles\welcome.txt", "r")
print(f.read())

with open("demofile.txt") as f:
print(f.read())

f = open("demofile.txt")
print(f.readline())
f.close()

with open("demofile.txt") as f:
    print(f.read(5))

with open("demofile.txt") as f:
    print(f.readline())

with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())

with open("demofile.txt") as f:
  for x in f:
    print(x)

#"a" - Append - will append to the end of the file
#"w" - Write - will overwrite any existing content

with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")
with open("demofile.txt") as f:
  print(f.read())

with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
with open("demofile.txt") as f:
  print(f.read())

import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")

