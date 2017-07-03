import sys
import os

module_name = sys.argv[1]
current_path = os.getcwd()
module_path = sys.argv[2]

os.chdir(module_path)
os.mkdir(module_name)
os.chdir(module_name)
open('__init__.py', 'a').close()
print "create module ", module_name