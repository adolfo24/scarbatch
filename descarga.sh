#!/bin/bash 
cd /home/ec2-user
wget "https://github.com/adolfo24/scarbatch/archive/master.zip"
unzip master.zip
rm master.zip
cd /home/ec2-user/scarbatch-master
chmod +x prueba.sh 
./prueba.sh