# Telegram Scheduled Message Bot

This Python script uses the [Telethon](https://github.com/LonamiWebs/Telethon) library to automate sending scheduled messages to a Telegram group at a specified interval.

## Features

- Sends a verification code to your Telegram account for login.
- Supports two-factor authentication (2FA).
- Reads the message content from a `message.txt` file.
- Allows user to select a group from their Telegram dialogs.
- Sends messages at regular intervals indefinitely.

## Prerequisites

- Python 3.7 or higher
- A Telegram account
- A Telegram API ID and hash ([Get it here](https://my.telegram.org/auth))

## Installation

1. **Clone the repository (or copy the script).**

   2. **Install required dependencies:**

      ```bash
      pip install -r requirements.txt
   
      
      python3 main.py
