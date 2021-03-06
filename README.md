# <img src="https://cdn.iconscout.com/icon/free/png-256/list-bullets-menu-format-formatting-items-6-3298.png" height="30" width="30"> sshmenu

<img src="img/sshmenu.png">

sshmenu is a *very* simple terminal tool that reads your ssh-config  
and renders an interactive menu with your ssh profiles listed

## Installation

Requires:
* python3
* pip

Install:

```bash
$ sudo pip install ssh-menu
```

Uninstall:

```bash
$ sudo pip uninstall ssh-menu
```

**Note:** sshmenu depends on a config file located in your *user-home*/.ssh folder  
You can find examples [here](https://www.ssh.com/ssh/config/)

## Alias

You can alias sshmenu to make it easier to use

Bash:
```bash
$ echo 'alias ssm="sshmenu"' >> ~/.bashrc
$ source ~/.bashrc
```

Zsh:
```bash
$ echo 'alias ssm="sshmenu"' >> ~/.zshrc
$ source ~/.zshrc
```

Now you can just enter `ssm` to open sshmenu

## TMUX

Checks if **TMUX** is running, and if so, it uses it.
When ssh starts, a window is created with the name **ssh:host**. If the window already exists, it switches to the existing window. 

add update environment to ~/.tmux.conf

    set-option -g update-environment "SSH_AUTH_SOCK SSH_CONNECTION DISPLAY"
     
## Docker

Running in docker (why? I don't know):

```bash
docker run -it -v $PWD/config:/root/.ssh/config antonjah/ssh-menu
```

## Todo

* Enable adding profiles
* Custom profile location
* Handle output even if session dies unexpectedly
