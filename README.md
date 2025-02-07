# IRC_socket

# IRC Client Script

This is a simple Python-based IRC (Internet Relay Chat) client that allows users to connect to an IRC server, join a channel, and either listen to or send messages or do both simultaneously.

## Features

- **Listen Mode**: Receives and displays messages from an IRC server in real-time.
- **Send Mode**: Sends user-inputted messages to an IRC server.
- **Both Modes**: Allows simultaneous listening and sending of messages using threading.

## Requirements

- Python 3.x
- Internet connection to connect to the IRC server.

## Usage

Run the script with the following command structure:

```bash
python3 irc.py [listen|send] <server> <port> <channel> <username>
