from shutil import which
import os 

print("Hello to the automated FTP server launcher")
print(" ----------------------------------------- ")

dependecies = ["ssh", "vsftpd", "filezilla"]

active_mode_port = str(input("enter active mode port: "))
commands_port = str(input("enter command's port: "))
user_name = str(input("enter a user name for the clients: "))
directory_name = str(input("enter directory name: "))
server_directory = str(input("enter the directory where u want to create your server : "))


config_data = """#Added by the Automated FTP launcher 
anonymous_enable=NO
local_enable=YES
write_enable=YES
pasv_min_port=5000
pasv_max_port=10000
local_root=/{}
chroot_local_user=YES
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd.chroot_list
allow_writeable_chroot=YES
local_umask=0002
rsa_cert_file=/etc/ssl/private/vsftpd.pem
rsa_private_key_file=/etc/ssl/private/vsftpd.pem
ssl_enable=YES
allow_anon_ssl=NO
force_local_data_ssl=YES
force_local_logins_ssl=YES
ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO
require_ssl_reuse=NO
ssl_ciphers=HIGH""".format(directory_name)


def start_services():
    status = os.system('systemctl is-active --quiet vsftpd')
    if status == 0:
        pass
    else:
        os.system("sudo systemctl enable --now vsftpd")
    
    os.system("sudo systemctl restart sshd")

def create_user(user_name):
    os.system("sudo adduser " + user_name)

def edit_files(user_name):
    with open("/etc/ssh/sshd_config", "a") as f:
        f.write("DenyUsers " + user_name)
    
    with open("/etc/vsftpd.conf", "a") as f:
        f.write(config_data)

    with open("/etc/vsftpd.chroot_list", "a") as f:
        f.write(user_name)
    
def open_ports(port_1, port_2):
    os.system("sudo ufw allow " + port_1 + "/tcp")
    os.system("sudo ufw allow " + port_2 + "/tcp")
    os.system("sudo ufw allow 990/tcp")
    os.system("sudo ufw allow 5000:10000/tcp")

def check_if_exist(dependecy):
    print("checking: " + dependecy)
    if (which(dependecy) == None):
        install_dependecy(dependecy)
    else:
        print("Done :)")

def install_dependecy(dependecy):
    print("installing : " + dependecy + "...")
    os.system("sudo apt install " + dependecy)

for dependecy in dependecies:
    check_if_exist(dependecy)


open_ports(active_mode_port, commands_port)
start_services()
create_user(user_name)

os.system("sudo mkdir /" + directory_name)
os.system("sudo chown " + user_name + " /" + directory_name)
os.system("sudo touch /etc/vsftpd.chroot_list")

edit_files(user_name)

os.system("sudo systemctl restart sshd")
os.system("sudo systemctl restart --now vsftpd")

os.system("sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/vsftpd.pem -out /etc/ssl/private/vsftpd.pem")
os.system("sudo systemctl restart --now vsftpd")

os.system("filezilla")
