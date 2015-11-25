#!/bin/bash
# init
# defaul folder 	/c/Users/houssem.fathallah/work/training/quickerio/
entties="$*"

entties_count="$#"

working_folder = ""

function redo(){
   echo "q to quit, r : reply"
   read action
   echo "$action"
   if [ "$action" == "r" ]; then 
		init
	else 
		echo "nothing to do, press [enter] to quit "
		quit
	fi
}
function quit (){
	read -p ''
}

function dowrok (){
	#!/bin/bash
	# bash trap command
	git add .
	# commit 
	git commit -m 'message !'
	git push heroku master 
	heroku open
	redo
	
}
function init(){
	echo "start init"
	#echo "$working_folder"
	#echo ${#working_folder}
	if  [ ${#working_folder} -eq 0 ] &&  [ "$entties_count" -eq 0 ]   ; then 
		echo "no foder specified , give me where your heroku folder"
		read working_folder
		echo "start working in >>> $working_folder"
		cd "$working_folder"
		dowrok 
	else 
		dowrok
	fi
}

init 
