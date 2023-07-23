# Braindump

![BrainDump](icon.png)

Braindump is a purposefully minimal text editor my nephew and I (at least) use to journal.

## Overview

You open it and it starts a new file for the current day. You can go to the next day by pressing ctrl + shift + f or the last one with ctrl + shift + b. To go to the present day you can press ctrl + shift + p. You can press ctrl + shift + s to save. It stores its data on disk at a path you specify (see below for more). It stores files like this:

  ➜ jg ~ cd Dropbox/Journal
  ➜ jg Journal tree

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

## What it looks like

A picture is worth a thousand words.

!(screenshot.png)

## How it works for me

It works for me inasmuch it instilled in me a daily writing habit and gave me a simple interface in which to review/add my thoughts.

* If it's Sunday and I think of something about work which I have a meeting on Wednesday about then I jump to Wednesday and write about it there so I can remember.

* I write every morning generally after gym/yoga, generally with a medium black Americano. I record what I get up to, what people said, and mostly important what I felt. I also ruminate on where I am going in life and so on.  I am an extremely deep/thoughtful person you see.

* I keep the file on Dropbox and thus they are backed up and easily searchable. I also have a simple program that reads this Dropbox directory and emails me the changes. One day, I'd like to print everything out and put it in a big spiral bound book. Maybe it could then be shown in the British Museum.

## Configuration

You can tell Braindump where to store files by creating a file "$HOME/.config/braindump.ini" with the path:

➜ jg ~ cat .config/braindump.ini
[Settings]
file_storage_directory = /home/jg/Dropbox/Journal

## Support

You are inherently worthy. Before you ever do, achieve, or acquire, you are worthy.
