## BUGswarm Tools README
Welcome to BUGswarm-Tools, a simple set of python scripts that allows users to access all the juicy information regarding their BUGswarm account without the need to use excessively long and frustrating 'curl' commands.

INSTALLATION:
In order to install BUGswarm Tools, simply clone this repository from github using the following command:

    git clone git@github.com:buglabs/bugswarm-tools.git

USAGE:
Before using any of the python scripts contained within BUGswarm Tools, you must run the following command, using your personal BUGswarm username and password:

    python init.py init <username> <password>

This script will generate a file called "swarm.cfg" within the package that will contain your API keys.  These API keys will be pulled from the various dependent scripts within BUGswarm Tools.

For each of the BUGswarm Tools scripts, simply run 'python <script name>' without any arguments to see what functions are available to you for that given script.

Note that the swarmtoolscore.py script does not contain any standalone functions. This file simply contains helper methods for the other scripts.  Once you know what function in a given script you would like to call, simply call 'python <script name> <function name>' followed by any parameters the function may require.

For example, to list all of the Swarms belonging to your user account, simply call:

    python swarm.py list

And to list the API keys associated with your user account, simply call:

    python api_keys.py list <username> <password>

