#!/bin/bash
set -e

write_file=y

ask_pass(){
	local pass
	local confirmation
	prompt=$1
	varname=$2
	read -p "$prompt: " -r -s pass
	echo
	read -p "$prompt confirmation: " -r -s confirmation
	echo
	if [ "$pass" != "$confirmation" ]; then
		echo 'Passwords missmatch, try again'
		ask_pass "$@"
	else
		eval "$varname=$pass"
	fi

}

read -p 'Database username: ' -r dbusername
ask_pass 'Database password' dbpassword
read -p 'InfluxDB username: ' -r idbusername
ask_pass 'InfluxDB password: ' idbpassword
ask_pass 'Application secret key (if empty it is generated randomly): ' appsecret

if [ -z "$appsecret" ]; then
	appsecret="$(python -c "import random; import string; print(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)))")"
fi


if [ -e "../wenuapi/secrets.py" ]; then
	while read -p 'Overwrite ../wenuapi/secrets.py? [Y/n]' write_file; do
		write_file=$(echo "$write_file" | tr '[:upper:]' '[:lower:]')
		if [ "$write_file" = y ] || [ "$write_file" = n ]; then
			break
		fi
	done
fi

if [ "$write_file" = y ]; then
	cat > ../wenuapi/secrets.py <<EOF
database_username = '${dbusername}'
database_password = '${dbpassword}'
influxdb_username = '${idbusername}'
influxdb_password = '${idbpassword}'

SECRET_KEY = '${appsecret}'
EOF
fi
