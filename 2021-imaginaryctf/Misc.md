
# Misc Challenges

Writeups in this file only give a brief description. 

### Imaginary
We need to solve 300 arithmethic expressions with imaginary numbers. The expressions could be parsed, because they have a well-defined and easy format, but the description even mentions `eval`. So, i changed `i` to `*i` (needed for sagemath), then imported sagemath (`sage.all`) and used `eval` on the code.
The fork bomb? If the string cointains `__`, I ignore it befor evaluating.

### Spelling Test
We need to find all wrongly written words. We used a python script: Open a looong wordlist, check every word if it exists, if not, check if there is a word with exactly 1 different letter. If yes, print the letter. We only had 2 false positives, that were clearly detectable reading the flag.

### Prisoner's Dilemma
When we connect via ssh to the remote server, we are put into a vim instead of a shell. And we need to somehow access a secret file with unknown name. However, `vim` is configured, to ignore important command.

```#!/usr/bin/env -S vim -u /dev/null +'set nocompatible' +'set directory=/tmp backupdir=/tmp' +'noremap : <nop>' +'noremap Q <nop>' +'noremap ! <nop>' +'inoremap quit <Esc>:qa!<cr>'```

So, no `:` (forbids e.g. `:tabe somefile`), `Q`, `!`(forbids running bash commands) and some more stuff.
After some time, I figured out, that I can open files under the current cursor with `<Ctrl+w> g f`. This sometimes does not work in the opened file after changing it. But I could open `/usr/bin/env` with this trick (yes it is a binary, but doesn't matter). And in the newly opened file, I can write any file and open it with the same key combination.
For a long time, I tried to access helpful files. I found the authorized_keys, bashrc and profile, but nothing helpful.
After more a lot of more googling, I found how to autocomplete paths in Insert Mode: [here](https://codeyarns.com/tech/2016-10-06-how-to-autocomplete-path-in-vim-insert-mode.html)
So: Open /usr/bin/env, type `/home/user/`, press `<Ctrl-X> <Ctrl-F>` and autocomplete with the secret file. Open it.

### Mazed
We are given a 4-dimensional grid with walls (`#`) and spaces (`.`) and need to go from start to the flag. This is not a vulnerability challenge but a programming challenge. My code can be found [here](https://github.com/DerBaer0/CTF-writeups/blob/main/2021-imaginaryctf/maze_exploit.py). It does a Depth First Search starting from the end to visit new places until it finds the start while keeping track of already visited places and how to get from there to the end.
