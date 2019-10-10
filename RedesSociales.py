import requests
import json
import sys
import os


from instagram.client import InstagramAPI
from flask import Flask, request
import time
app = Flask(__name__, static_folder='.', static_url_path='')


class User:
	def __init__(self):
		self.id=None
		self.username=None
		self.fullName=None
		self.followers=None
		self.posts=[]

	def loadSelf(self,data):
		self.id=data["id"]
		self.username=data["username"]
		self.fullName=data["full_name"]
		self.followers=int(data["counts"]["followed_by"])

	def loadPosts(self,data):
		for post in data:
			aux=Post()
			aux.load(post,self.followers)
			self.posts.append(aux)

	def objToDic(self):
		data={"id":self.id,"username":self.username,"fullName":self.fullName,"followers":self.followers,"post":[]}

		for post in self.posts:
			data["post"].append({"id":post.id,"likes":post.likes,"efficiency":post.efficiency,"link":post.link})

		return data

class Post:
	def __init__(self):
		self.id=None
		self.likes=None
		self.link=None
		self.efficiency=None

	def load(self,data,followers):
		self.id=data["id"]
		self.likes=int(data["likes"]["count"])
		self.link=data["link"]
		self.calculateEfficiency(followers)


	def calculateEfficiency(self,followers):
		num=round((self.likes/followers)*100,2)
		self.efficiency=str(num)+"%"

class Social:
	def __init__(self):
		#self.clientId="cffe00f905f14083bbeafc9292ab23da"
		#self.clientSecret="ec8ee6a2ccaa4025ab420de95e4730d0"

		self.token="1821160367.1677ed0.1fef08ca4eda4420b9a78cba01a04a57";
		self.urlPost="https://api.instagram.com/v1/users/self/media/recent?access_token="+self.token
		self.urlUser="https://api.instagram.com/v1/users/self/?access_token="+self.token
		self.session = requests.session()

	def get(self):
		r = self.session.get(self.urlUser)
		data=json.loads(r.content)["data"]
		user=User()
		user.loadSelf(data)

		r = self.session.get(self.urlPost)
		data=json.loads(r.content)["data"]

		user.loadPosts(data)

		#login_data = dict(client_id=str(self.clientId))
		#r = self.session.post(self.urlAuth,login_data)
		#api = InstagramAPI(client_id=self.clientId, client_secret=self.clientSecret)
		#print(data)


		return {"data":user.objToDic()}

@app.route("/")
def index():
	return "Instagram API"
@app.route("/instagram", methods=["GET", "POST"])
def log():
	save=Social()
	return save.get()

if __name__ == "__main__":
    app.run(debug=True)