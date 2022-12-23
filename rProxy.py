#!/usr/bin/env python3
try:
    import paramiko
    import getpass
    import sys
    from colorama import Fore
    import os

except:
    print('make shure you installed paramiko and colorama!')


startText = f'''{Fore.CYAN}

            (☞ ͡° ͜ʖ ͡°)☞ 𝓻𝓟𝓻𝓸𝔁𝔂 ♥♥

{Fore.RESET}'''

print(startText)

help = 'rproxy [add, remove] [user] [host]\n\n'





def connectToHost(connect, serverName, port_proxy, port_server, passwd, user, hostname):



    # nginx reverse proxy configuration
    # Edit this part to add aditional configuration to Nginx
    #
    nginxConfig = "server { server_name "+ serverName + "; location / { proxy_pass http://localhost:" + port_proxy + "/; proxy_set_header X-Real-IP \$remote_addr; proxy_set_header Host \$host; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto https; proxy_redirect off; } error_page 502 /50x.html; location = /50x.html {root /usr/share/nginx/html;}}"
    #
    ###########################################

    # connecting server to reverse proxy via ssh
    connect.connect(hostname ,port=22, username=user, password=passwd, look_for_keys=False, allow_agent=False) # connecting ssh

    # adding configuration to nginx config file 
    connect.exec_command(f'echo "{nginxConfig}" >> /etc/nginx/conf.d/nginx.conf') # executing command
    # reloading nginx on remote server
    connect.exec_command(f'nginx -s reload')
    connect.close()

    # starting reverse ssh tunnel
    os.system(f'tmux new -d -s {serverName.replace(".","_")} "ssh -R {port_proxy}:localhost:{port_server} {user}@{hostname}"')
    os.system(f'tmux send-keys -t {serverName.replace(".","_")} "{passwd}" enter')





try:
    test = sys.argv[1]

except IndexError:
    print(help)
    exit()


if sys.argv[1] == 'add':

    serverName = input('[ ] Enter new server name (sub.domane.com): ')
    
    # gets pors from user
    port_server = input('[ ] Enter port you want to expose on local machine: ')
    port_proxy = input('[ ] Enter port you want to tunnel to: ')
    
    # password for ssh server
    passwd = getpass.getpass('[ ] Enter ssh-password of the reverse proxy: ')
    # keyPasswd = input('[ ] Enter name of your tunnel')


    # checks if user and host are specyfied. Throws error if not specyfied 
    try:
        user = sys.argv[2]
        host = sys.argv[3]

    except IndexError as err:
        print(f'{Fore.RED}\n\n\n[Err] {err}\n{Fore.RESET}')
        print(help)
    

    # checks if ports are provided
    if port_server == None or port_proxy == None:
        print('[Err] No specyfied ports')
        print(help)



    # setting up connection to server
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    

    # calls connection function
    connectToHost(client, serverName, port_proxy, port_server, passwd, user, host)

    
