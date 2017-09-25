#!/bin/bash
SECRETS=../wenuapi/secrets.py

username=$(grep -E '^database_username' "$SECRETS" | cut -d= -f2 | tr -d \ \'\")
password=$(grep -E '^database_password' "$SECRETS" | cut -d= -f2 | tr -d \ \'\")

echo "-${username}-"
echo "-${password}-"

cat | mysql -u root <<EOF
DROP DATABASE IF EXISTS wenuapi;
CREATE DATABASE wenuapi;
GRANT ALL ON wenuapi.* TO '${username}' IDENTIFIED BY '${password}';
EOF
