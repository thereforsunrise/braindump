# Braindump

![BrainDump](icon.png)

Braindump is a purposefully minimal text editor my nephew and I (at least) use to journal.

## Overview

It simply presents a full-screen distraction-free editor which you can write any notes in. Perodically these notes will be emailed to you with the subject set to the date and time of which they were sent. I use it to make sporadic notes throughout the day which I review later in my email client. Simple and works for me.

## Configuration

There is a very simple configuration file which should be auto-created when you first start Braindump.


    jamesgray@moon braindump % cat /Users/jamesgray/Library/Preferences/Python/braindump/braindump.ini
    [Email]
    sender_email = <>
    receiver_email = <>
    smtp_server = <>
    smtp_port = 587
    smtp_tls = True
    smtp_ssl = False
    username =
    password =
