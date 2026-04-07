# Custom Server Tools

```sh
python -m venv _test
. _test/bin/activate.fish
python3 -m pip install -r requirements.txt
```

- Make a folder on the client
- put some files in it like forge, mods resource packs, etc.

## mcrcon

```sh
Commands list:

/ban: Prevents the specified player from using this server
/ban-ip: Prevents the specified IP address from using this server
/banlist: View all players banned from this server
/defaultgamemode: Set the default gamemode
/deop: Takes the specified player's operator status
/difficulty: Sets the game difficulty
/gamemode: Changes the player to a specific game mode
/give: Gives the specified player a certain amount of items
/help: Shows the help menu
/kick: Removes the specified player from the server
/kill: Commits suicide, only usable as a player
/list: Lists all online players
/me: Performs the specified action in chat
/op: Gives the specified player operator status
/pardon: Allows the specified player to use this server
/pardon-ip: Allows the specified IP address to use this server
/plugins: Gets a list of plugins running on the server
/reload: Reloads the server configuration and plugins
/save-all: Saves the server to disk
/save-off: Disables server autosaving
/save-on: Enables server autosaving
/say: Broadcasts the given message as the sender
/seed: Shows the world seed
/setworldspawn: Sets a worlds's spawn point. If no coordinates are specified, the player's coordinates will be used.
/spawnpoint: Sets a player's spawn point
/stop: Stops the server, with optional reason
/tell: Sends a private message to the given player
/time: Changes the time on each world
/timings: Records timings to see performance of the server.
/tp: Teleports the given player (or yourself) to another player or coordinates
/version: Gets the version of this server including any plugins in use
/whitelist: Manages the list of players allowed to use this server
```
