#!/usr/bin/env python3

import re
import sys
from os import name, system, execvp, environ
from os.path import expanduser
from subprocess import check_call, check_output
from collections import OrderedDict
from bullet import Bullet, colors
from keyword import


TMUX_ = "TMUX" in environ

# TODO: Add configuration file option for menu theme
def main():
    ssh_config = expanduser("~/.ssh/config")
    hosts_ = _get_ssh_hosts(ssh_config)

    host = _menu(hosts_)
    _clear()
    if host == 'exit':
        sys.exit(0)

    try:
        print("Connecting to \"{}\" ...".format(host))
        _tmux_ssh_window(host)
        execvp("ssh", args=["ssh", host])
    except Exception as e:
        sys.exit(e)


def _menu(hosts, parent='', separator='.', pfx1='* ', pfx2='  ', bullet='>'):
    host_menu_ = list(OrderedDict.fromkeys(
        [pfx1 + sp_host[0] if len(sp_host) > 1 else pfx2 + sp_host[0] for sp_host in
         [host.split(separator) for host in
          [host[len(parent):] for host in
           hosts if host.startswith(parent)]]]))
    if parent == '':
        exit_menu_ = ['exit']
    else:
        exit_menu_ = ['back', 'exit']
    cli = Bullet(
        choices=host_menu_ + exit_menu_,
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

        if choise_ == 'back':
            return ''
        elif choise_ == 'exit':
            break
        elif choise_.find(pfx1) >= 0:
            result = _menu(hosts, parent + choise_[len(pfx1):] + separator, separator, pfx1, pfx2)
            if result != '':
                return result
        else:
            return parent + choise_[len(pfx1):]
    return 'exit'


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
            if key.lower() == "host" and value != "*":
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


# TMUX decorator
def tmux(func):
    def wrapper(*args, **kwargs):
        if TMUX_:
            func(*args, **kwargs)

    return wrapper


@tmux
def _tmux_ssh_window(host):
    check_call(["tmux", "display-message", "Connecting to \"{}\" ...".format(host)])
    tmux_windows_ = check_output(["tmux", "list-windows", "-F", "#{window_index},#{window_name}"]) \
        .decode('utf-8').split()
    ids_ = [id_ for (id_, host_) in [window_.split(',') for window_ in tmux_windows_] if host_ == "ssh:" + host]
    if len(ids_) > 0:
        execvp("tmux", args=["tmux", "select-window", "-t", ids_[0]])
    else:
        execvp("tmux", args=["tmux", "new-window", "-n", "ssh:" + host, "ssh " + host])


@tmux
def _tmux_display_message(message):
    check_call(["tmux", "display-message", message])


if __name__ == "__main__":
    main()
