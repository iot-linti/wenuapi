#!/bin/bash
set -e

read -p 'Rabbit user: ' user
read -r -s -p 'Rabbit password: ' password
read -p 'Rabbit vhost: ' vhost
read -p 'Rabbit wenu tasks Tag:' tag

rabbitmqctl add_user "$user" "$password"
rabbitmqctl add_vhost "$vhost"
rabbitmqctl set_user_tags "$user" "$tag"
rabbitmqctl set_permissions -p "$vhost" "$user" ".*" ".*" ".*"

echo 'URL: '
echo "broker_url = \'amqp://$user:<password>@$(hostname -f):5672/$vhost\'"
