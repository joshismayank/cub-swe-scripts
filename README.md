The script was written for python 2.7

*install pip: sudo apt install python-pip\
*install pandas: pip install pandas\
*install gitpython: pip install gitpython\
*install xlrd: pip install xlrd\

Download assignment:\
&nbsp- this script uses git ssh to download repositories\
&nbsp&nbsp- to download any assignment, make sure you add the assignment to the script. Please refer to 'Add assignment section'\
	- to enable ssh for git, go through the documentation: 'https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh'\
	- github id's of student: this can be downloaded from github classroom. login to github classroom -> go to desired classroom -> go to settings -> roster management -> download\
	- command line parameters to be provided:\
		* --download_repos\
		* --for_assignment "1"\
		* --github_roster "path/to/roster"\
		* --path_to_ssh "path/to/your/ssh/file/which/you/added/to/github/account"\
		* --destination_direc "path/to/folder/where/repos/are/to/be/saved" (this is optional)\
	- if assignment also needs to be added, add following extra parameters in command line:\
		* --add\
		* --assignment_no "1"\
		* --assingment_name "Example assignment"\

Add assignment:\
	- the assignments are stored in the form of dictionary in the variable assignments with key as assignment number and value as assignment name. The data type of assignment number is integer.\
	- the assignment name should exactly match the title of the assignment in the github classroom. All the special characters and uppercase characters should be put as is.\
	- the assignment can be added using command line arguments:\
		* --add\
		* --assignment_no "1"\
		* --assingment_name "Example assignment"\
	- the assignment added this way will not be accessible next time the script is used. So, always add the assignment while downloading the assignment\

Email comments:\
	- this requires you to turn on less secure access for your google account. it can be done as per this documentation: 'https://support.google.com/accounts/answer/6010255?hl=en/' \
	- get the comments in swe-grades.xlsx file\
	- the grades and comments for assignment 'n' sholud be stored in the 'assignment' sheet of the xlsx file. Like comments od asssignment 2 should be in 'assignment2' sheet\
	- the comments should be stored under the column name 'comments' (all lowercase)\
	- if the colorado-id of a student is alph1234, then mail will be sent to alph1234@colorado.edu\
	- the colorado-id of students (alph1234 and not alph1234@colorado.edu) should be stored under the column 'SIS Login ID' (match exact case)\
	- the subject of emails being sent out can be changed by updating the variable 'subject' in the function 'email_comments'\
	- command line parameters to be provided:\
		* --email_comments\
		* --email_id "your@email.id"\
		* --for_assignment "1"\
	- the script will ask for password to authenticate the email address\

Extract grades:\
	- this creates an .xlsx file which can be uploaded directly to canvas\
	- download swe-grades.xlsx from the drive\
	- supply: --for_assignment (the assignment number) and --assignment_name (name of assignment in canvas)\
	- import the formed xlsx into canvas\
