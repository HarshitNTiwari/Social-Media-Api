from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from datetime import datetime
import uuid

from api import app
from api import database as db
from api.models.users import User
from api.models.posts import Post


def authenticate(email, password):
	user = db.get_user(email)
	if user and user.password == password:
		return user

def identity(payload):
    user_id = payload['identity']
    print("payload identity: ", user_id)
    return db.get_user(user_id)


jwt = JWT(app, authenticate, identity)


@app.route('/api/follow/<string:id>', methods=['POST'])
@jwt_required()
def follow(id):
	user_id = current_identity.id
	print("current identity: ",current_identity)
	response = db.follow_user(user_id, id)
	return response

@app.route('/api/unfollow/<string:id>', methods=['POST'])
@jwt_required()
def unfollow(id):
	user_id = current_identity.id
	response = db.unfollow_user(user_id, id)
	return response


@app.route('/api/user', methods=['GET'])
@jwt_required()
def getUser():
	user_id = current_identity.id
	user = db.get_user(user_id)
	if user:
		response = {'name': user.name, 'No. of followers': len(user.follower), 'No. of followings': len(user.following)}
		return jsonify(response)
	return jsonify({"Message": "User not found"})

@app.route('/api/posts', methods=['POST'])
@jwt_required()
def addPost():
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		post_data = request.json
	user_id = current_identity.id
	post = Post(str(uuid.uuid1()), user_id, post_data['title'], post_data['desc'], str(datetime.now()), [], 0)
	post = db.add_post(post)
	if post:
		response = {'Post-ID': post.post_id, 'Title': post.title, 'Description': post.desc, 'Created Time': post.created_at}
		return jsonify(response)
	return jsonify({"Message": "Title or Desc not found"}) 

@app.route('/api/posts/<string:id>', methods=['DELETE'])
@jwt_required()
def deletePost(id):
	user_id = current_identity.id
	response = db.delete_post(id, user_id)
	return response 

@app.route('/api/like/<string:id>', methods=['POST'])
@jwt_required()
def likePost(id):
	user_id = current_identity.id
	print(id)
	response = db.like_post(id, user_id)
	return response

@app.route('/api/unlike/<string:id>', methods=['POST'])
@jwt_required()
def unlikePost(id):
	user_id = current_identity.id
	response = db.unlike_post(user_id, id)
	return response

@app.route('/api/comment/<string:id>', methods=['POST'])
@jwt_required()
def postComment(id):
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		comment_data = request.json
	comment = comment_data['comment']
	user_id = current_identity.id
	response = db.add_comment(user_id, id, comment)
	return response 

@app.route('/api/posts/<string:id>', methods=['GET'])
@jwt_required()
def getPost(id):
	post = db.get_post(id)	
	if post:
		response = {"No. of likes": post.likes_count, "Array of comments": post.comments}
		return jsonify(response)
	return jsonify({"message": "Post Id not found"})

# @app.route('/api/all_posts', methods=['GET'])
# @jwt_required()
# def get():
# 	user_id = current_identity.id
# 	get_all_posts(user_id)