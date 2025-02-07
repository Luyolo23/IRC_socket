import socket
import sys
import threading


def listen(server, port, channel, username):
    """
    Listens for messages from the IRC server and prints them to the console.
    """
    # Create a socket for the IRC connection
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the IRC server
        irc.connect((server, port))
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Send NICK and USER commands to identify ourselves to the server
    irc.send(f"NICK {username}\r\n".encode('utf-8'))
    irc.send(f"USER {username} 0 * :{username}\r\n".encode('utf-8'))

    # Join the specified channel
    irc.send(f"JOIN {channel}\r\n".encode('utf-8'))

    # Buffer to store incomplete messages
    buffer = ""

    # Main loop to listen for messages
    while True:
        # Receive data from the server
        data = irc.recv(4096).decode('utf-8', errors='ignore')

        # If no data is received, the connection is closed
        if not data:
            break

        # Append received data to the buffer
        buffer += data

        # Process complete messages (ending with \r\n)
        while '\r\n' in buffer:
            # Split the buffer into a complete line and the remaining buffer
            line, buffer = buffer.split('\r\n', 1)
            print(f"Line: {line}")

            # Respond to PING messages to keep the connection alive
            if line.startswith('PING'):
                irc.send(f"PONG {line.split()[1]}\r\n".encode('utf-8'))
                continue

            # Break the loop if the server sends a QUIT or ERROR message
            if 'QUIT' in line or 'ERROR' in line:
                break

            # Ignore messages sent by ourselves
            if line.startswith(f":{username}!"):
                continue

            # Process PRIVMSG (private messages) from other users
            if 'PRIVMSG' in line:
                parts = line.split(' ')
                sender = parts[0].split('!')[0][1:]  # Extract the sender's username
                message = ' '.join(parts[3:])[1:]   # Extract the message content
                print(f'<{sender}> {message}')

    # Close the connection when done
    irc.close()


def send(server, port, channel, username):
    """
    Sends messages to the IRC server based on user input.
    """
    # Create a socket for the IRC connection
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the IRC server
        irc.connect((server, port))
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Send NICK and USER commands to identify ourselves to the server
    irc.send(f"NICK {username}\r\n".encode('utf-8'))
    irc.send(f"USER {username} 0 * :{username}\r\n".encode('utf-8'))

    # Join the specified channel
    irc.send(f"JOIN {channel}\r\n".encode('utf-8'))

    # Main loop to send messages
    while True:
        # Get user input
        message = input()

        # If the user types /quit, send a QUIT command and exit
        if message.lower() == '/quit':
            irc.send(f"QUIT :Goodbye\r\n".encode())
            break

        # Send the message to the channel
        irc.send(f"PRIVMSG {channel} :{message}\r\n".encode())

    # Close the connection when done
    irc.close()


if __name__ == "__main__":
    """
    Main entry point for the script. Handles command-line arguments and starts the appropriate function.
    """
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 6:
        print('Usage: python3 irc.py [listen|send|both] <server> <port> <channel> <username>')
        sys.exit(1)

    # Parse command-line arguments
    command = sys.argv[1]
    server = sys.argv[2]
    port = int(sys.argv[3])
    channel = sys.argv[4]
    username = sys.argv[5]

    # Start the appropriate function based on the command
    if command == 'listen':
        listen(server, port, channel, username)
    elif command == 'send':
        send(server, port, channel, username)
    elif command == 'both':
        # Start both listening and sending in separate threads
        threading.Thread(target=listen, args=(server, port, channel, username)).start()
        threading.Thread(target=send, args=(server, port, channel, username)).start()
    else:
        print("Invalid command. Use 'listen', 'send', or 'both'.")
        sys.exit(1)