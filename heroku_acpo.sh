#!/bin/bash
# init
# defaul folder /c/Users/houssem.fathallah/work/training/quickerio/

function pause(){
   read -p "$*"
}
function dowrok (){
	#!/bin/bash
	# bash trap command
	git add .
	# commit 
	git commit -m 'message !'
	git push heroku master 
	heroku open
	pause 'Press [Enter] key to continue...'
}
if [ "$#" -eq 0 ]; then 
	echo "give me where your heroku folder"
	read folder
	echo "$folder"
	cd "$folder"
	dowrok 
else 
	dowrok
	# ...
	# call it
fi 
