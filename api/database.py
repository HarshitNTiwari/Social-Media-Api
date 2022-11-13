from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from api.models.users import User
from api.models.posts import Post

client = MongoClient("mongodb+srv://admin:admin123@socialapidb.lst3pgp.mongodb.net/?retryWrites=true&w=majority")

social_media_db = client.get_database("SocialApiDB")
users_collection = social_media_db.get_collection("users")
posts_collection = social_media_db.get_collection("posts")


def follow_user(user_id, follow_id):
	if user_id != follow_id:
		user_data = users_collection.find_one({'_id': user_id}) 
		print("user_data found")
		followings = user_data['following']
		
		user_data = users_collection.find_one({'_id': follow_id})
		if user_data:
			if follow_id not in followings:
				users_collection.update_one({'_id': user_id}, {'$addToSet':{'following': follow_id}})
				users_collection.update_one({'_id': follow_id}, {'$addToSet':{'follower': user_id}})
				return "OK"
			return "Follow failed : user_id already following follow_id"
		return "Follow failed : follow_id not found"
	return "Follow failed : follow_id same as user_id"

def unfollow_user(user_id, unfollow_id):
	if user_id != unfollow_id:
		user_data = users_collection.find_one({'_id': user_id}) 
		followings = user_data['following']

		if unfollow_id in followings:
			users_collection.update_one({'_id': user_id}, {'$pull':{'following': unfollow_id}})
			users_collection.update_one({'_id': unfollow_id}, {'$pull':{'follower': user_id}})
			return "OK"
		return "Unfollow failed : unfollow_id not in following list of user_id"
	return "Unfollow failed : unfollow_id same as user_id"

def get_user(user_id):
	user_data = users_collection.find_one({'_id': user_id})
	if user_data:
		return User(user_data['_id'], user_data['password'], user_data['name'], user_data['following'], user_data['follower'], user_data['liked_posts']) 
	return None


def add_post(post):
	if post.title and post.desc:
		posts_collection.insert_one({'_id': post.post_id, 'created_by': post.created_by, 'title': post.title, 'desc': post.desc, 'created_at': post.created_at, 'comments': post.comments, 'likes_count': post.likes_count})
		return post
	return None

def delete_post(post_id, user_id):
	post = posts_collection.find_one({'_id': post_id})
	if post and post['created_by'] == user_id:
		posts_collection.delete_one({'_id': post_id})
		return "OK"
	return "Post not found"


def like_post(post_id, user_id):
	post = posts_collection.find_one({'_id': post_id})
	print(post)
	if post:
		user_data = users_collection.find_one({'_id': user_id})
		liked_posts_list = user_data['liked_posts']
		if post_id not in liked_posts_list:
			users_collection.update_one({'_id': user_id}, {'$addToSet': {'liked_posts': post_id }})
			posts_collection.update_one({'_id': post_id}, {'$inc': {'likes_count': 1}})
			return "OK"
		else:
			return "Post already in liked posts list of user_id"
	return "Post ID not found"

def unlike_post(user_id, post_id):
	post = posts_collection.find_one({'_id': post_id})
	if post:
		user_data = users_collection.find_one({'_id': user_id})
		liked_posts_list = user_data['liked_posts']
		if post_id in liked_posts_list:
			users_collection.update_one({'_id': user_id}, {'$pull': { 'liked_posts': post_id }})
			posts_collection.update_one({'_id': post_id}, {'$inc': {'likes_count': -1}})
			return "OK"
		else:
			return "Post not in liked posts list of user_id"
	return "Post ID not found"


def add_comment(user_id, post_id, comment):
	post = posts_collection.find_one({'_id': post_id})
	if post:
		posts_collection.update_one({'_id': post_id}, {'$push': {'comments': comment}})
		return "OK"
	return "Post ID not found"


def get_post(post_id):
	post = posts_collection.find_one({'_id': post_id})
	if post:
		return Post(post['_id'], post['created_by'], post['title'], post['desc'], post['created_at'], post['comments'], post['likes_count'])
	return None
