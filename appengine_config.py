from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
	app = SessionMiddleware(app, cookie_key="youdefowilln0tgu3ssthissEcReTkey3v3r")
	return app