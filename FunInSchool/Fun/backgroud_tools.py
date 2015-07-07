#!/usr/local/bin/python

import os
import sys
#from FunInSchool import School,Teacher,Province,City,District,Kid,Parents,ParentsGroup,Moment


func_name_list=[]
func_list={}


def cmd(func):
    func_name = func.func_name
    func_name_list.append(func_name)
    func_list[func_name] = func
    return func
@cmd
def updateSchoolStatus():
    print 2

@cmd
def updateTeacherStatus():
    print sys.argv[2:]

def main():
    calling_tool_name=sys.argv[1]
    print func_name_list
    #print func_list
    #if calling_tool_name in func_name_list:
	#func_list[calling_tool_name]()

if __name__ == '__main__':
    main()
