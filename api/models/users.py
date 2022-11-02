from werkzeug.security import check_password_hash

class User():
	def __init__(self, email, password, name, follower, following, liked_posts):
		self.id = email
		self.password = password
		self.name = name
		self.follower = follower
		self.following = following
		self.liked_posts = liked_posts


	def get_id(self):
		return self.email 

	# def check_password(self, password_input):
	# 	return check_password_hash(self.password, password_input)