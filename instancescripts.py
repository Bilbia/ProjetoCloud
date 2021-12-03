postgres_script="""
#cloud-config

runcmd:
- cd /
- sudo apt update -y
- sudo apt install postgresql postgresql-contrib -y
- sudo su - postgres
- sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
- sudo -u postgres psql -c "CREATE DATABASE tasks;"
- sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE tasks TO cloud;"
- sudo echo "listen_addresses = '*'" >> /etc/postgresql/10/main/postgresql.conf
- sudo echo "host all all 0.0.0.0/0 trust" >> /etc/postgresql/10/main/pg_hba.conf
- sudo ufw allow 5432/tcp -y
- sudo systemctl restart postgresql
"""

django_script="""
#cloud-config

runcmd:
- cd /home/ubuntu 
- sudo apt update -y
- git clone https://github.com/Bilbia/tasks.git
- cd tasks
- sed -i "s/node1/POSTGRES_IP/g" ./portfolio/settings.py
- ./install.sh
- sudo ufw allow 8080/tcp -y
- sudo reboot
"""