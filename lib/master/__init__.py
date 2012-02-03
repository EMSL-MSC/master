"""This is a library for the MASTER project"""

def debug(msg):
	pass

def basicdebug(msg):
	print "DEBUG:"+msg

config = {
	"config_file"       : "/etc/mcp.conf",
    "privileged_conf"   : "/etc/mcp-priv.conf",
	"server_url"        : "http://master:627",
	"sark_modules"      : ("all",),
	"database_server"   : "",
	"database_name"     : "master",
	"database_user"     : "master",
	"database_password" : "",
	"database_min_connections" : 3,
	"database_max_connections" : 5,
	"decode_dimms"      : "/usr/bin/decode-dimms",
	"hpacucli"          : "/usr/sbin/hpacucli",
	"mcp_port"          : 627,
	"mcp_host_authorization" : True,
	"web_interface"     : False,
	"web_directory"     : "/usr/share/mcp/web",
	"mcp_pid_file"      : "/var/run/mcp.pid"
}

def load_config():
    load_config_file("config_file")

def load_privileged_config():
    load_config_file("privileged_conf")

def load_config_file(param):
    """Loads the configuration file defined in config[param]"""

    global config

    try:
		crap={}
		exec open(config[param]) in crap, config
		for (k,v) in config.items():
			debug("Config: "+str(k)+" => "+str(v))
    except IOError:
		debug("Error Loading Config file: "+config["config_file"])


