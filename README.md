#BUGswarm Tools

BUGswarm Tools is a simple set of python scripts that utilize http requests to wrap up both the [Configuration](http://developer.bugswarm.net/configuration_api.html)
and [Participation](http://developer.bugswarm.net/participation_api.html) APIs of BUGswarm in an effort to minimize the time spent using said APIs. BUGswarm tools eliminates
the need for curl commands and allows developers to quickly and easily start configuring and participating in swarms. 

##Installation

```shell
git clone git@github.com:buglabs/bugswarm-tools.git
cd bugswarm-tools
./init.py init USERNAME PASSWORD
```

For the USERNAME and PASSWORD, use the credentials from your Bug Labs account.

If you are running zsh, you may want to add the following function to your .zshrc:

```javascript
function swarm() {
  $HOME/code/buglabs/bugswarm-tools/$1.py $*[2,$#-1]   
}
```

This will let you run commands like `swarm user_resources create` from anywhere, instead of `/path/to/user_resources.py create`.

##Usage

For each of the python scripts in the root of the bugswarm-tools repository, simply run `./SCRIPT_NAME` without any arguments or `./SCRIPT_NAME --help` to view the usage.
This will provide you with a list of potential methods you can use with the given script.

Running `./SCRIPT_NAME METHOD_NAME --help` will provide you with the usage information for the given method.
