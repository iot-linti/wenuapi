#!/bin/sh
PREFIX=/usr/local

# Configuramos el path donde encontrar el script en la definición del
# servicio para SystemD
sed -r "s!@PREFIX@!$PREFIX!g" meteo2mqtt.service.template > meteo2mqtt.service


install -m 755 meteo2mqtt.py "$PREFIX/bin/meteo2mqtt"
install -m 644 meteo2mqtt.service /etc/systemd/system/
pip install -r requirements.txt

systemctl --system enable meteo2mqtt.service
