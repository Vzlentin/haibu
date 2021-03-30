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
fi

MEDIA_PATH=$(grep MEDIA_PATH .flaskenv | cut -d= -f2)

sudo ln -sfn /opt/haibu/app/anime/static $MEDIA_PATH/Anime
sudo ln -sfn /opt/haibu/app/scans/static $MEDIA_PATH/Scans

cd /opt/haibu/utils
python3 syncdb.py

sudo systemctl daemon-reload
sudo systemctl restart haibu.service
