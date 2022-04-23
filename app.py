#!/usr/bin/env python3
import sys
import os
import tarfile
from tempfile import template
import docker
import yaml
import argparse

watcher_template=lambda path, *mode: "{} {} /etc/incron/cmd/update $@/$#".format(path, ''.join([*map(str, mode)]))

client = docker.from_env()

def copy_to(src, dst):
    name, dst = dst.split(':')
    container = client.containers.get(name)

    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open('/tmp/secret/' + srcname + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open('/tmp/secret/' + srcname + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)
    
def restart_container (name):
    container = client.containers.get(name)
    container.restart()

def write_incron_rules (watcher, config_group, mode, incron):
    with open(incron, mode) as cmd:
        cmd.write(watcher_template(watcher['file_to_watch'], config_group['mode']) + '\n')
        cmd.close()

def init_rules(config, incron):
    rules=[]
    i = 0
    for watcher in config["watchers"]:
        print(watcher['name'])
        os.system('mkdir -p '+watcher['file_to_watch']+ ' /tmp/secret/')
        [config_group]=[*filter(lambda x: x['group_name'] == watcher['group'] , config['config'])]
        print("[RULES]: "+watcher_template(watcher['file_to_watch'], config_group['mode']))
        rules.append(watcher_template(watcher['file_to_watch'], config_group['mode']))
        print("[RULES]: "+rules[len(rules) - 1])
        write_incron_rules (watcher, config_group, 'w' if i==0 else 'a+', incron)
        if i == 0: i+=1

def make_copy (config, src):
    find_src=[*filter(lambda x: src.startswith(x['file_to_watch']), config['watchers'])]
    if len(find_src):
        os.system('echo Waiting ...')
        c_dst=find_src[0]['container']['name'] + ':' + find_src[0]['container']['path']
        copy_to(src, c_dst)
        print('[PROVISION] File `{}` as been push to the {}'.format(src, c_dst))
    #copy_to(src, dst)
    #restart_container(c_id)
    # TEST        
    #for watcher in config["watchers"]:
        #os.system("cp -Rv /test-file {}".format(watcher['file_to_watch']))
        #os.system("/etc/incron/cmd/update {}".format(watcher['file_to_watch']))
        #dst = watcher['container']['name'] + ":" + watcher['container']['path']
        #src = watcher['file_to_watch']
        #copy_to(src, dst)
        #restart_container(watcher['container']['name'])
    

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", help="Default template is locate on /etc/template.watcher.yml")
    parser.add_argument("--config", help="Default incron config is locate on /etc/incron.d/config")
    parser.add_argument("--provide", help="Provide repo[ulrs] to a container")
    return parser.parse_args()

if __name__ == "__main__":
    opts=cli()
    template = '/etc/template.watcher.yml'
    incron = '/etc/incron.d/config'
    if opts.template: template = opts.template
    if opts.config: incron = opts.config
    with open(template, 'r') as file:
        config=yaml.safe_load(file.read())
        if opts.template: init_rules(config, incron)
        if opts.provide: make_copy(config, opts.provide)
        file.close()

    #yaml.dump(yaml.load())
    #[src, dst]=[opt for opt in sys.argv[1:] if opt]
    #dst=dst if dst.endswith('/') else str(dst) + '/'
    #copy_to(src, dst)
    #for data in sys.stdin:
    #    c_id, c_path = data.split('_')
    #    print(c_id)
    #    print(client.containers.get(c_id).__dict__)
