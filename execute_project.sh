gnome-terminal -e "zsh -c 'python proxy/main.py ; zsh;'"

gnome-terminal -e "zsh -c 'python server/server.py 5555 localhost:5556 files1; zsh;'"

gnome-terminal -e "zsh -c 'python server/server.py 5557 localhost:5556 files2; zsh;'"

gnome-terminal -e "zsh -c 'python server/server.py 5558 localhost:5556 files3; zsh;'"