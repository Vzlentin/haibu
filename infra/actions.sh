#!/bin/sh

if [ ! -d "/opt/haibu" ]
then
	git clone https://github.com/vzlentin/haibu
	sudo mv haibu /opt/
	sudo chown -R pi:pi /opt/haibu
fi

cd /opt/haibu

if [ ! -f "/opt/haibu/app.db" ]
then
	python3 infra/createdb.py
fi

pip3 install -r requirements.txt

sudo mv /opt/haibu/infra/haibu.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start haibu.service
