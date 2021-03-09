import threading

class RequestMiddleware(object):
	
	thread_local = threading.local()

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# Almacenamos en el usuario que esta en el request
		self.thread_local.user = request.user
		self.thread_local.path = request.path
		self.thread_local.request = request
		response = self.get_response(request)
		self.thread_local.response = response
		return response