# apache-web-log
A website for showing apache logs for small site admins. Features a basic
dashboard and a full list of all log entries. Parses and stores all entries in a
sqlite database. Authentication is single hardcoded password. Supposed to not be so
fancy (for now).

# Install
0. `git clone` this repo
1. `pip install -r requirements.txt`
2. Copy example-config.cfg to config.cfg. Edit the SECRET_KEY and PASSWORD values
to something less predictable.
