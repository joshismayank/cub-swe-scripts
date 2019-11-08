<pre>
The script was written for python 2.7

* install pip: sudo apt install python-pip
* install pandas: pip install pandas
* install gitpython: pip install gitpython
* install xlrd: pip install xlrd

Download assignment:
- this script uses git ssh to download repositories
- to enable ssh for git, go through the documentation: 'https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh'
- github id's of student: this can be downloaded from github classroom. login to github classroom -> go to desired classroom -> go to settings -> roster management -> download
	
Email comments:
- this requires you to turn on less secure access for your google account. it can be done as per this documentation: 'https://support.google.com/accounts/answer/6010255?hl=en/'
- get the comments in swe-grades.xlsx file
- the grades and comments for assignment 'n' sholud be stored in the 'assignment' sheet of the xlsx file. Like comments od asssignment 2 should be in 'assignment2' sheet
- the comments should be stored under the column name 'comments' (all lowercase)
- if the colorado-id of a student is alph1234, then mail will be sent to alph1234@colorado.edu
- the colorado-id of students (alph1234 and not alph1234@colorado.edu) should be stored under the column 'SIS Login ID' (match exact case)
- the subject of emails being sent out can be changed by updating the variable 'subject' in the function 'email_comments'
- the script will ask for password to authenticate the email address

Extract grades:
- this creates an .csv file which can be uploaded directly to canvas
- download swe-grades.xlsx from the drive
- import the formed csv into canvas
</pre>
