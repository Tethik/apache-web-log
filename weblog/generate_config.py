import ConfigParser

print "[Configure paranoia]"

config = ConfigParser.RawConfigParser()
config.add_section('Paranoia')
config.set('Paranoia', 'logfile', raw_input("logfile: "))

filename = raw_input("filename: ")

with open(filename, 'wb') as configfile:
    config.write(configfile)
