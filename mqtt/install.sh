# https://mosquitto.org/download/
# https://mosquitto.org/blog/2013/01/mosquitto-debian-repository/


wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key

cd /etc/apt/sources.list.d/

wget http://repo.mosquitto.org/debian/mosquitto-jessie.list
wget http://repo.mosquitto.org/debian/mosquitto-stretch.list
wget http://repo.mosquitto.org/debian/mosquitto-buster.list


apt-get update
apt-cache search mosquitto
apt-get install mosquitto

