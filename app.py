#!/usr/bin/env python3
import sys
import os
import tarfile
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

if __name__ == "__main__":
    with open('./template.watcher.yml', 'r') as file:
        config=yaml.safe_load(file.read())
        for watcher in config["watchers"]:
            print(watcher['name'])
            [config_group]=[*filter(lambda x: x['group_name'] == watcher['group'] , config['config'])]
            print("[RULES]: "+watcher_template(watcher['file_to_watch'], config_group['mode']))
        file.close()
    #yaml.dump(yaml.load())
    #[src, dst]=[opt for opt in sys.argv[1:] if opt]
    #dst=dst if dst.endswith('/') else str(dst) + '/'
    #copy_to(src, dst)
    #for data in sys.stdin:
    #    c_id, c_path = data.split('_')
    #    print(c_id)
    #    print(client.containers.get(c_id).__dict__)