#!/bin/python

import sys
import pandas as pd
import os
import re
import argparse
from git import Repo
from IPython import embed

assignments = {}

def add_assignment(assignment_no, assignment_name):
    """
    adds and stores assignment names in assignments dict
    """
    if assignment_no in assignments:
        print("The assignment {} is mapped as the assignment number {}. Overwriting").format(assignments[assignment_no],assignment_no)
    assignments[assignment_no] = assignment_name


def download_assignment(assignment_no,filename,path_to_ssh):
    """
    downloads repo's of all students for assignement specified by assignment number
    """
    if assignment_no not in assignments:
        print("No such assignment exists in 'assignments'. Try adding assignment with --add. Exiting")
        sys.exit()
    
    curr_assign = assignments[assignment_no]
    curr_assign = curr_assign.lower()
    git_url_assign = '-'.join(re.findall('\w+',curr_assign))+'-'
    git_url_prefix = 'git@github.com:cu-swe4s-fall-2019/'
    git_url_postfix = '.git'
   
    unsuccessful_git_clone = []

    try:
        df = pd.read_csv(filename)
        if 'github_username' not in df.columns:
            print("github_username column does not exist in {}. Exiting").format(filename)
            sys.exit()
        df_new = df['github_username']
        for row in df_new.iteritems():
            user = row[1]
            if user is None or isinstance(user, float):
                continue
            repo_dir = git_url_assign + user
            git_url = git_url_prefix + repo_dir + git_url_postfix
            curr_env = {}
            curr_env["GIT_SSH_COMMAND"] = "ssh -i "+path_to_ssh
            try:
                Repo.clone_from(git_url,"assignment5/"+repo_dir,env=curr_env)
            except:
                unsuccessful_git_clone.append(user)
    except IOError:
        print("could not open file {}").format(filename)
        sys.exit()
    except Exception as e:
        print("could not download repos {}",e)
        sys.exit()
        
    if len(unsuccessful_git_clone) is 0:
        print('all repos cloned')
    else:
        print('could not clone repo\'s for:')
        for user in unsuccessful_git_clone:
            print(user)    


parser = argparse.ArgumentParser("swe-assignment")
parser.add_argument("--add", action = "store_true", help="add name of new assignment with: --assignment_no and --assignment_name")
parser.add_argument("--download_repos", action = "store_true", help="give assignment_no with: --for_assignment")
parser.add_argument("--assignment_no", help="integer")
parser.add_argument("--assignment_name", help="string: complete name as displayed in title of github classroom assignment")
parser.add_argument("--destination_direc", help="string: full path of folder where repos need to be downloaded (default: repos will be downloaded to current directory)")
parser.add_argument("--for_assignment", help="integer: to download repos for this assignment_no")
parser.add_argument("--path_to_ssh", help="string: your ssh file which has been registered with github for ssh conections")
parser.add_argument("--github_roster", help="string: name of csv file containing github id's for which assignment is to be downloaded (with column header as github_username)")
args = parser.parse_args()
if args.add:
    try:
        int(args.assignment_no)
    except:
        print("assignment_no should be integer")
        sys.exit()
    if args.assignment_no is None:
        print("assignment_no should can not be none")
        sys.exit()
    if type(args.assignment_name) is not str or args.assignment_name is None:
        print("assignment_name should be non-none string")
        sys.exit()
    add_assignment(args.assignment_no,args.assignment_name)
if args.download_repos:
    try:
        int(args.for_assignment)
    except:
        print("for_assignment should be integer")
        sys.exit()
    if args.for_assignment is None:
        print("for_assignment should can not be none")
        sys.exit()
    if type(args.github_roster) is not str or args.github_roster is None:
        print("using file `classroom_roster.csv` as default for github id's")
        args.github_roster = "classroom_roster.csv"
    if type(args.destination_direc) is not str or args.destination_direc is None:
        print("using current location to download folder")
        args.destination_direc = "assignment"+args.assignment_no+"/"
    if type(args.path_to_ssh) is not str or args.path_to_ssh is None:
        print("could not find path to ssh file")
        sys.exit()
    download_assignment(args.for_assignment,args.github_roster,args.path_to_ssh,args.destination_direc)
