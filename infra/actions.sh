#!/bin/sh

if [ ! -d "/opt/haibu" ]
then
	git clone https://github.com/vzlentin/haibu
	sudo mv haibu /opt/
	sudo chown -R pi:pi /opt/haibu
	pip3 install -r /opt/haibu/requirements.txt
	sudo cp /opt/haibu/infra/haibu.service /etc/systemd/system/
else
	cd /opt/haibu
	git pull
	sudo rm app.db
fi

cd /opt/haibu/infra
python3 createdb.py

sudo systemctl daemon-reload
sudo systemctl start haibu.service
