#!/bin/bash

gnome-terminal -e "zsh -c 'python server.py 5555 localhost:5556 files1; zsh;'"

gnome-terminal -e "zsh -c 'python server.py 5557 localhost:5556 files2; zsh;'"

gnome-terminal -e "zsh -c 'python server.py 5558 localhost:5556 files3; zsh;'"

gnome-terminal -e "zsh -c 'python server.py 5559 localhost:5556 files4; zsh;'"

gnome-terminal -e "zsh -c 'python server.py 5560 localhost:5556 files5; zsh;'"