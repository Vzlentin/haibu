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

MEDIA_PATH=$(grep MEDIA_PATH /opt/haibu/.flaskenv | cut -d= -f2 | sed "s/\"//g")

sudo ln -sf $MEDIA_PATH/Anime /opt/haibu/app/anime/static
sudo ln -sf $MEDIA_PATH/Scans /opt/haibu/app/scans/static

cd /opt/haibu/utils
python3 syncdb.py

sudo systemctl daemon-reload
sudo systemctl restart haibu.service
