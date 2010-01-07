"""This is a library for the MASTER project"""

def debug(msg):
	pass

def basicdebug(msg):
	print "DEBUG:"+msg

config = {
	"config_file"       : "/etc/mcp.conf",
	"server_url"        : "http://localhost:627",
	"sark_modules"      : ("all",),
	"database_server"   : "",
	"database_name"     : "master",
	"database_user"     : "master",
	"database_password" : "",
	"database_min_connections" : 3,
	"database_max_connections" : 5,
	"decode-dimms"      : "/usr/bin/decode-dimms",
	"hpacucli"          : "/usr/sbin/hpacucli",
	"mcp_port"          : 627,
	"mcp_host_authorization" : True,
	"web_interface"     : False,
	"web_directory"     : "/usr/share/mcp/web"
}

def load_config():
	global config

	try:
		crap={}
		exec open(config["config_file"]) in crap, config
		for (k,v) in config.items():
			debug("Config: "+str(k)+" => "+str(v)) 
	except IOError:
		debug("Error Loading Config file: "+config["config_file"])


