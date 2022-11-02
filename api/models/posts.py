
class Post():
	def __init__(self, post_id, created_by, title, desc, created_at, comments, likes_count):
		self.post_id = post_id
		self.created_by = created_by
		self.title = title
		self.desc = desc 
		self.created_at = created_at
		self.comments = comments
		self.likes_count = likes_count 