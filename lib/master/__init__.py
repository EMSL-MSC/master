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
	"database_min_connections" : "3",
	"database_max_connections" : "5",
	"hpacucli"          : "/home/efelix/hpacucli/bld/.hpacucli",
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


