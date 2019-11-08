#!/bin/python

import sys
import pandas as pd
import os
import re
import smtplib
import argparse
import getpass
from git import Repo
from IPython import embed
from pandas import ExcelWriter
from pandas import ExcelFile
from pandas import ExcelWriter
from email.mime.text import MIMEText

assignments = {}

def add_assignment(assignment_no, assignment_name):
    """
    adds and stores assignment names in assignments dict
    """
    if assignment_no in assignments:
        print("The assignment {} is mapped as the assignment number {}. Overwriting").format(assignments[assignment_no],assignment_no)
    assignments[assignment_no] = assignment_name


def download_assignment(assignment_no,curr_assign,filename,path_to_ssh,destination_direc):
    """
    downloads repo's of all students for assignement specified by assignment number
    """
    
    curr_assign = curr_assign.lower()
    git_url_assign = '-'.join(re.findall('\w+',curr_assign))+'-'
    git_url_prefix = 'git@github.com:cu-swe4s-fall-2019/'
    git_url_postfix = '.git'
   
    if destination_direc is None or isinstance(destination_direc, float):
        destination_direc = "assignment"+str(assignment_no)+"/"

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
                Repo.clone_from(git_url,destination_direc+repo_dir,env=curr_env)
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


def email_comments(email_id,assignment_no,assignment_name):
    print "enter password"
    password = getpass.getpass()
    sheet = "assignment"+str(assignment_no)
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    try:
        s.login(email_id,password)    
    except Exception as e:
        print("could not authenticate gmail. Exiting "+str(e))
        sys.exit()
    try:
        df = pd.read_excel("swe-grades.xlsx", sheet_name = sheet)
    except:
        print("failed to access sheet {} of swe-grades.xlsx".format(sheet))
    if 'comments' not in df.columns:
        print("could not find 'comments' column")
        sys.exit()
    if 'SIS Login ID' not in df.columns:
        print("could not find 'SIS Login ID' (canvas login id) column")
        sys.exit()
    subject = 'CSCI7000-SWE: comments for '+sheet
    for index, row in df.iterrows():
        to_mail = row['SIS Login ID']
        comment = row["comments"]
        if comment is not None and not isinstance(comment,float) and to_mail is not None and not isinstance(to_mail, float):
            to_mail = to_mail+"@colorado.edu"
            msg = MIMEText(comment)
            msg['Subject'] = subject
            msg['From'] = email_id
            msg['To'] = to_mail
            s.sendmail(email_id, to_mail, msg.as_string())
    s.quit()


def extract_grades(assignment_no,assignment_name):
    sheet = "assignment"+str(assignment_no)
    try:
        df = pd.read_excel("swe-grades.xlsx", sheet_name = sheet)
    except:
        print("failed to access sheet {} of swe-grades.xlsx".format(sheet))
    if 'total' not in df.columns:
        print("could not find 'total' column")
        sys.exit()
    if 'SIS Login ID' not in df.columns:
        print("could not find 'SIS Login ID' (canvas login id) column")
        sys.exit()
    if 'Student' not in df.columns:
        print("could not find 'Student' column")
        sys.exit()
    if 'ID' not in df.columns:
        print("could not find 'ID' column")
        sys.exit()
    if 'SIS User ID' not in df.columns:
        print("could not find 'SIS User ID' column")
        sys.exit()
    if 'Section' not in df.columns:
        print("could not find 'Section' column")
        sys.exit()
    df.drop(df.columns.difference(['Student','ID','SIS Login ID', 'SIS User ID', 'Section', 'total']), 1, inplace=True)
    df.rename(columns={'total': assignment_name}, inplace=True)
    output = "assignment"+str(assignment_no)+".csv"
    df.to_csv(output, index=False)


print("What do you want to do:")
print("1. Download repos")
print("2. Email comments")
print("3. Extract grades")
print("Option (1 or 2 or 3) ?")
option = raw_input().strip()
if option == "1":
    print("assignment no for which repos need to be downloaded:")
    assignment_no = int(raw_input().strip())
    print("assignment name for which repos need to be downloaded (name should exactly match the name in github):")
    assignment_name = raw_input().strip()
    print("roster containing github ids of student (should be downloaded from github). To use default file 'classroom_roster.csv' press 'd'") 
    github_roster = raw_input().strip()
    if github_roster == "d" or github_roster  == "D":
        github_roster = "classroom_roster.csv"
    print("location of folder where you want to download the repos. To download at current location press 'd'")
    destination_direc = raw_input().strip()
    if destination_direc == "d" or destination_direc == "D":
        destination_direc = "assignment" + str(assignment_no) + "/"
    print("path to your ssh file linked with github account")
    path_to_ssh = raw_input().strip()
    download_assignment(assignment_no,assignment_name,github_roster,path_to_ssh,destination_direc)
elif option == "2":
    print("assignment no for which comments need to be mailed:")
    assignment_no = int(raw_input().strip())
    print("comments will be extracted from sheet 'assignment{}' of 'swe-grades.xlsx'".format(assignment_no))
    print("assignment name for which comments need to be mailed (name should exactly match the name in github):")
    assignment_name = raw_input().strip()
    print("your email id")
    email_id = raw_input().strip()
    email_comments(email_id,assignment_no,assignment_name)
elif option == "3":
    print("in 3")
    print("assignment no for which grades need to be extracted:")
    assignment_no = int(raw_input().strip())
    print("grades will be extracted from sheet 'assignment{}' of 'swe-grades.xlsx'".format(assignment_no))
    print("assignment name for which grades need to be extracted (name should exactly match the name in canvas):")
    assignment_name = raw_input().strip()
    extract_grades(assignment_no,assignment_name)
else:
    print("invalid option")
