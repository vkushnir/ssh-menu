#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from os import name, system, execvp
from os.path import expanduser

from bullet import Bullet, colors
from collections import OrderedDict


def main():
    ssh_config = expanduser("~/.ssh/config")
    hosts_ = _get_ssh_hosts(ssh_config)

    host_ = _menu(hosts_, pfx1='✺ ', bullet='➤')
    _clear()
    if host_ == '':
        sys.exit(0)

    try:
        print("Connecting to \"{}\" …".format(host_))
        execvp("ssh", args=["ssh", host_])
    except Exception as e:
        sys.exit(e)


def _menu(hosts, parent='', separator='.', pfx1='* ', pfx2='  ', bullet='>'):
    host_menu_ = list(OrderedDict.fromkeys(
        [pfx1 + sp_host[0] if len(sp_host) > 1 else pfx2 + sp_host[0] for sp_host in
         [host.split(separator) for host in
          [host[len(parent):] for host in
           hosts if host.startswith(parent)]]]))

    cli = Bullet(
        choices=host_menu_ + ['exit'],
        indent=0,
        align=4,
        margin=2,
        bullet=bullet,
        bullet_color=colors.bright(colors.foreground["cyan"]),
        background_on_switch=colors.background["black"],
        word_color=colors.bright(colors.foreground["red"]),
        word_on_switch=colors.bright(colors.foreground["red"]),
        pad_right=5
    )

    while True:
        _clear()
        if parent != '':
            print("\n    Choose ssh profile from {}:".format(parent[:-1]))
        else:
            print("\n    Choose ssh profile:")
        choise_ = cli.launch()

        if choise_ == 'exit':
            return ''
        elif choise_.find(pfx1) >= 0:
            result = _menu(hosts, parent + choise_[len(pfx1):] + separator, separator, pfx1, pfx2)
            if result != '':
                return result
        else:
            return parent + choise_[len(pfx1):]


def _get_ssh_hosts(config_dir):
    """ Parse lines from ssh config """
    try:
        with open(config_dir, "r") as fh_:
            lines = fh_.read().splitlines()
    except IOError:
        sys.exit("No configuration file found.")

    hosts_ = []
    for line in lines:
        kv_ = _key_value(line)
        if len(kv_) > 1:
            key, value = kv_
            if key.lower() == "host":
                hosts_.append(value)
    return hosts_


def _key_value(line):
    """ Parse lines and make sure it's not commented """
    no_comment = line.split("#")[0]
    return [x.strip() for x in re.split(r"\s+", no_comment.strip(), 1)]


def _clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")
