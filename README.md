### Clients-and-Server-Chat-Application

# My Chat Program

What’s this about?
Yo, I built this awesome chat program with Python! It’s not a website or a phone app—it’s a program that runs on your computer with a cool window you can click around in. It’s a basic chat program built with Python, Tkinter for the GUI, and TCP sockets, letting a server and a bunch of clients talk to each other right away over a network. There’s a server that lets people join and chat, and a client where you type messages and see what everyone’s saying. The server can send messages to everybody or just one person privately, and the client makes a “ding” sound when a new message pops up (if you’ve got the sound file).
I made this to mess around with networking stuff like sockets, make a GUI with Tkinter, and figure out how to let lots of people chat at once with threading. It’s like my own mini WhatsApp, and I had a ton of fun putting it together!
What’s cool about it

Server:
Lets a bunch of people chat together at once.
Shows when someone joins or leaves.
You can send messages to everyone or just one person.
Has a window with a chat history and buttons to control stuff.


Client:
You pick a username and join the server.
Send messages and see everyone’s messages with the time they sent it.
Plays a “ding” sound (from notify.wav) for new messages, if you’ve got Pygame.
Has a window for typing and reading messages.


Both parts look fun with bright colors and a few emojis!

How to get it going
Stuff you need

Python 3 on your computer (it’s free and easy to set up).
Tkinter (usually comes with Python, so you’re probably good).
Pygame for the sound (optional, but cool). Get it by typing:pip install pygame


A file called notify.wav in the same folder as the client (only if you want sound). Any .wav file works!

Files you’ll see

server.py: Runs the server where everyone connects.
client.py: Runs the client so you can chat.
notify.wav: A sound file for message alerts (you can skip it).

How to start it

Kick off the server:

Open a terminal or command prompt.
Go to the folder with server.py.
Type:python server.py


A window pops up saying “Server started. Waiting for clients…”. Sweet!


Start a client:

Open another terminal.
Go to the folder with client.py.
Type:python client.py


A box asks for your username. Type something fun and hit OK.
If the server’s running, you’ll join and see “Welcome to the chat!”.


Add more people:

Run client.py again in a new terminal to add more folks. Everyone needs their own username.


Chat away:

In the client, type a message and click “Send 💬”.
In the server, send messages to everyone or just one person with the buttons.


Shut it down:

Click “Close Server” in the server window to stop it.
Click “Close ❌” in the client window to bounce.



How it works

The server uses sockets to talk to clients over a network (on your computer, using 127.0.0.1 and port 5555).
Threading lets the server handle lots of people at once, so no one’s waiting.
Tkinter makes the windows with text boxes, buttons, and all that.
The client plays a sound with Pygame when a message comes in, if you’ve got notify.wav.

Good to know

You gotta start the server before anyone can join.
If you close the server, clients see a message saying it’s gone.
No notify.wav or Pygame? No worries, the client works without sound.
This runs on your computer (localhost). To use it over the internet, you’d need to tweak the IP in the code.

Try it out

Run server.py. The server window says “Server started”.
Run client.py, type “Alex” as your username. Alex joins!
Run client.py again, type “Sam”. Sam’s in too.
Alex types “Yo Sam!” and clicks Send. Sam sees “Alex 🗣️: Yo Sam! [14:30]” and hears a ding.
The server types “Hey guys!” and clicks “Send to All”. Alex and Sam both see it.

Why I made it
I thought it’d be super fun to build my own chat program and learn how networking and GUIs work. This showed me how stuff like WhatsApp handles messages. Adding private messages and that ding sound was so cool!
If something breaks

Client won’t join? Make sure the server’s running. Check you’re using 127.0.0.1 and port 5555.
No ding sound? Check if Pygame’s installed and notify.wav is in the client’s folder.
Getting errors? The program shows pop-ups if something’s wrong, like a bad connection. Check the pop-up for clues.

Ideas to make it cooler

Let people send pics or files.
Make it work over the internet, not just my computer.
Add a password so only friends can join.
Save the chat so you can read it later.

Thanks for checking out my chat program! Try it out and tell me what you think. It’s been a blast making this!

