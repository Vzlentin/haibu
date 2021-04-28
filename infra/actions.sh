#!/bin/sh

if [ ! -d "/opt/haibu" ]
then
	git clone https://github.com/vzlentin/haibu
	sudo mv haibu /opt/
	sudo chown -R pi:pi /opt/haibu
else
	cd /opt/haibu
	git pull
fi

pip3 install -r /opt/haibu/requirements.txt

MEDIA_PATH=$(grep MEDIA_PATH /opt/haibu/.flaskenv | cut -d= -f2 | sed "s/\"//g")

sudo ln -sn $MEDIA_PATH/Anime /opt/haibu/app/anime/static
sudo ln -sn $MEDIA_PATH/Scans /opt/haibu/app/scans/static

cd /opt/haibu/utils
python3 syncdb.py

sudo cp /opt/haibu/infra/haibu.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now haibu.service

cron="00 12 * * *   pi      /usr/bin/python3 /opt/haibu/utils/rss_scrap.py >> /opt/haibu/test.log"

grep -qF "$cron" /etc/crontab  || echo "$cron" | sudo tee --append /etc/crontab
