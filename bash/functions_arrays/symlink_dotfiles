#!/bin/bash

# Description: Link dotfiles to home directory

link_dot_file() {
    local src="$1"
    local dest="$2"
    ln -sf "$src" "$dest"
    echo "Linked: $dest"
}

dotfiles=("bashrc" "vimrc")

for file in "${dotfiles[@]}"; do
    link_dot_file "$HOME/dotfiles/$file" "$HOME/.$file"
done

ln -sf ~/dotfiles/starship.toml ~/.config/starship.toml

echo "Done!"
