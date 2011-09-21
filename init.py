#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import ConfigParser
import sys
import json
import base64

def usage(script_name):
    print "%s [init] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def init(user_id, password):
    config = ConfigParser.ConfigParser()
    config.add_section("User Information")
    config.add_section("Keys")
    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

    swarmtoolscore.set_user_info(user_id)
    swarmtoolscore.set_keys(user_id, password)

def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "init":
        opt_usage = "usage: \n  %s USER_ID PASSWORD"%(sys.argv[1])
        opt_usage += "\n\n  *USER_ID: Your BUGnet account User ID." \
                    +"\n  *PASSWORD: Your BUGnet account password."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        if len(args) != 3:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        user_id = args[1]
        password = args[2]
        init(user_id, password)
    else:
        usage(sys.argv[0])

main()
