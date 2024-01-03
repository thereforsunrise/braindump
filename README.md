# Braindump

![BrainDump](icon.png)

Braindump is a purposefully minimal text editor my nephew and I (at least) use to journal.

## Overview

You open it and it starts a new file for the current day. You can go to the next day by pressing ctrl + shift + f or the last one with ctrl + shift + b. To go to the present day you can press ctrl + shift + p. You can press ctrl + shift + s to save. It has a concept of multiple notebooks which you can switch between with ctrl + shift + g and ctrl + shift + n.

It will also save every 30 seconds by default and/or when you move between days. It stores its data on disk at a path you specify (see below for more). It stores files like this:

    ➜ jg braindump (main) ✗ cat ~/.config/braindump.ini

    ➜ jg Journals cd ~/Dropbox/Journals

    ➜ jg Journals tree -L 1       
    .
    ├── Personal
    └── Work

    ➜ jg Personal cd ~/Dropbox/Journals/Personal

    ➜ jg Personal tree

    ├── 2022
    │   └── 07
    │       └── 22.txt
    ├── 2023
    │    ├── 01
    │   │   └── 22.txt
    │   ├── 02
    │   │   └── 22.txt
    │   ├── 07
    │   │   ├── 08.txt

## Configuration

You can tell Braindump where to store files by creating a file "$HOME/.config/braindump.ini" with the path:

    ➜ jg ~ cat ~/.config/braindump.ini
    [Settings]
    # where to store files
    notebooks_base_directory = /home/jg/Dropbox/Journals
    # save files after interval
    save_interval = 30
