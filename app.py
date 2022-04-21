#!/usr/bin/env python3
import sys
import os
import tarfile
from tempfile import template
import docker
from isort import file
import yaml

watcher_template=lambda path, *mode: "{} {} /etc/incron/cmd/update $@/$#".format(path, ''.join([*map(str, mode)]))

client = docker.from_env()

def copy_to(src, dst):
    name, dst = dst.split(':')
    container = client.containers.get(name)

    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)
    
def restart_container (name):
    container = client.containers.get(name)
    container.restart()

def init_rules():
    rules=[]
    incron, template='./incron/incron.d/config', './template.watcher.yml'
    with open(template, 'r') as file:
        config=yaml.safe_load(file.read())
        for watcher in config["watchers"]:
            print(watcher['name'])
            [config_group]=[*filter(lambda x: x['group_name'] == watcher['group'] , config['config'])]
            print("[RULES]: "+watcher_template(watcher['file_to_watch'], config_group['mode']))
            dst = watcher['container']['name'] + ":" + watcher['container']['path']
            src = watcher['file_to_watch']
            copy_to(src, dst)
            restart_container(watcher['container']['name'])
            rules.append(watcher_template(watcher['file_to_watch'], config_group['mode']))
            print("[RULES]: "+rules[len(rules) - 1])
        
        with open(incron, 'a+') as cmd:
            cmd.write("\n"+"\n".join(rules))
            
            cmd.close()
        file.close()

if __name__ == "__main__":
    init_rules()
    #yaml.dump(yaml.load())
    #[src, dst]=[opt for opt in sys.argv[1:] if opt]
    #dst=dst if dst.endswith('/') else str(dst) + '/'
    #copy_to(src, dst)
    #for data in sys.stdin:
    #    c_id, c_path = data.split('_')
    #    print(c_id)
    #    print(client.containers.get(c_id).__dict__)
