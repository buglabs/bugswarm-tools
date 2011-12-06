#BUGswarm Tools

BUGswarm Tools is a simple set of python scripts that utilizes http requests to wrap up both the [Configuration](http://developer.bugswarm.net/configuration_api.html)
and [Participation](http://developer.bugswarm.net/participation_api.html) APIs of BUGswarm in an effort to minimize the time spent using said APIs. BUGswarm tools eliminates
the need for curl commands and allows developers to quickly and easily start configuring and participating in swarms. 

##Installation

Using the username and password from your Bug Labs account, run the following shell commands.

```shell
git clone git@github.com:buglabs/bugswarm-tools.git
cd bugswarm-tools
./init.py init USERNAME PASSWORD
```

##Usage

For each of the python scripts in the root of the bugswarm-tools repository, simply run `./SCRIPT_NAME` without any 
arguments or `./SCRIPT_NAME --help` to view the usage. This will provide you with a list of potential methods you 
can use with the given script.

Running `./SCRIPT_NAME METHOD_NAME --help` will provide you with the usage information for the given method.

**Note:** The configuration portion of BUGswarm Tools (all scripts with the exception of `consume.py` and `produce.py`)
has a 1:1 relationship with the methods documented at the [Developer Portal](http://developer.bugswarm.net/configuration_api.html).
Developers may find it useful to consult that documentation when using BUGswarm Tools.

###Example

Let's say you want to create a new configuration API key (either because you don't have one yet or you want to 
replace your current key with a fresh one). By running `./api_keys.py` with no arguments or `./api_keys.py --help`, 
we are given the following usage output:

```
./api_keys.py [create|list] 

Use './api_keys.py [method] --help' for a method's usage and options.
```

This output lets us know that there are two methods we can use with this script, 'create' and 'list'. Since this is the
'api_keys.py' script, it is safe to assume that these methods refer to creating and listing a user's API keys. Now, since
we want to create an API key, we will run `./api_keys.py create --help` to view the usage for the 'create' method. Doing
so produces the following output:

```
Usage: 
  create PASSWORD [options]

  *PASSWORD: Your Bug Labs account password.

Options:
  -h, --help            show this help message and exit
  -t KEY_TYPE, --type=KEY_TYPE
                        Specify the type of API key you wish to create. Valid
                        types; 'configuration', 'participation' (both keys are
                        created if no type specified).
```

This usage output shows us that, in order to use this method, we must give it our Bug Labs password as an argument. Additionally,
we may choose to use the 'KEY_TYPE' option to specify which type of key we wish to create. Since both keys are created
by default and we only wish to create the configuration key, we will use this option to specify the key type.

So, to create our configuration API key, we will run `./api_keys.py create PASSWORD -t configuration`, where 'PASSWORD' will be filled in
with your Bug Labs account password. Running this command produces the following output:

```javascript
{
    "created_at": "2011-11-17T16:09:54.890Z", 
    "key": "31ca73d1cfcda8d70c348a577afc1862c49b1a16", 
    "status": "active", 
    "type": "configuration", 
    "user_id": "barberdt"
}

```

Well there you go. We just created our configuration API key. Using the remaining scripts and methods in the same way will
allow you to quickly and easily develop on the BUGswarm platform. Good luck!
