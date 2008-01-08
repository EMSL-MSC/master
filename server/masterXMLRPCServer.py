import SimpleXMLRPCServer
import sys


class MasterServerRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
	def report_error(self,code, message):
		self.send_response(code)
		response = 'Client Not Authorized'
		self.send_header("Content-type", "text/plain")
		self.send_header("Content-length", str(len(response)))
		self.end_headers()
		self.wfile.write(message)
		# shut down the connection
		self.wfile.flush()
		self.connection.shutdown(1)

	def do_POST(self):
		try:
			if self.authFunction() == True:
				SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.do_POST(self)
			else:
				self.report_error(403,"Client Not Authorized")
		except NameError, e:
			self.report_error(500,"Auth function Not Specified"+str(e))


class MasterXMLRPCServer(SimpleXMLRPCServer.SimpleXMLRPCServer):
	functions = []
	def __init__(self,addr,authFunction):
		MasterServerRequestHandler.authFunction = authFunction
		SimpleXMLRPCServer.SimpleXMLRPCServer.__init__(self,addr,MasterServerRequestHandler)
		
	def serve_forever(self):
		for i in self.functions:
			self.register_function(i,"master.%s" % i.__name__)
		self.register_introspection_functions()
		SimpleXMLRPCServer.SimpleXMLRPCServer.serve_forever(self)

	def _dispatch(self, method, params):
		try:
			return SimpleXMLRPCServer.SimpleXMLRPCServer._dispatch(self,method,params)
		except:
			import traceback
			etype, value, tb = sys.exc_info()
			print "Exception Caught:\n%s%s" % ("".join(traceback.format_tb(tb)), traceback.format_exception_only(etype,value)[0]),
			raise

def rpc(func):
	MasterXMLRPCServer.functions.append(func)
	return func
