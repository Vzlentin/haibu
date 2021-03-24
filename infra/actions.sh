#!/bin/sh

if [ ! -d "/opt/haibu" ]
then
	git clone https://github.com/vzlentin/haibu
	sudo mv haibu /opt/
	sudo chown -R pi:pi /opt/haibu
fi

if [ ! -f "/opt/haibu/app.db" ]
then
	python3 /opt/haibu/infra/createdb.py
fi

sudo mv /opt/haibu/infra/haibu.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start haibu.service
