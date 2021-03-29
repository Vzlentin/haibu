#!/bin/sh

if [ ! -d "/opt/haibu" ]
then
	git clone https://github.com/vzlentin/haibu
	sudo mv haibu /opt/
	sudo chown -R pi:pi /opt/haibu
	cd /opt/haibu/infra
	python3 createdb.py
	pip3 install -r /opt/haibu/requirements.txt
	sudo mv /opt/haibu/infra/haibu.service /etc/systemd/system/
else
	cd /opt/haibu
	git pull
fi

sudo systemctl daemon-reload
sudo systemctl start haibu.service
