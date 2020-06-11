# spacevim pissing me off --
# moving to neovim-init / blackarch --
# orig --
# https://github.com/Optixal/neovim-init.vim

# refs --
# https://github.com/neoclide/coc.nvim
# https://github.com/VundleVim/Vundle.vim

Note:
Make sure you have node installed and symlinked --

helix :: /tmp » ls -l /opt/node/bin/nodejs
lrwxrwxrwx 1 root root 18 Jun 10 11:32 /opt/node/bin/nodejs -> /opt/node/bin/node*
helix :: /tmp » 

Start Setup -- 
- mkdir -p ~/.config/nvim
- yain neovim python3 python3-pip git curl exuberant-ctags python2-neovim python-pynvim python2-pynvim ruby-neovim
- python3 -m pip install virtualenv
- python3 -m virtualenv -p python3 ~/.config/nvim/env
- source ~/.config/nvim/env/bin/activate
- pip install neovim==0.2.6 jedi psutil setproctitle yapf
- deactivate
- curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
- curl -fLo ~/.fonts/Iosevka\ Term\ Nerd\ Font\ Complete.ttf --create-dirs https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/Iosevka/Regular/complete/Iosevka%20Term%20Nerd%20Font%20Complete.ttf
- echo "alias vim='nvim'" >> ~/.zshrc

Install vundle --
- git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim  

Fetch init.vim --
- curl -sk 'https://raw.githubusercontent.com/cdowns71/stuffz/master/configs/nvim/init.vim' -O ~/.config/nvim/init.vim

- nvim +PlugInstall +UpdateRemotePlugins +qall
- cp init.vim init.vim.save

Anything else ?
Commands --

https://github.com/Optixal/neovim-init.vim/blob/master/README.md
https://github.com/Optixal/.vim/blob/master/reference/commands_vim.txt

Other Deps ( language autocompletion ) --
sudo npm install -g neovim
:CheckHealth

Make sure all is fine and mcdadny --

Install Laguage packs --
ref: 
https://github.com/neoclide/coc.nvim/wiki/Using-coc-extensions

:CocInstall coc-python
:CocInstall coc-solargraph 



