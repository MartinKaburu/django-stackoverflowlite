from json import loads, dumps
import json
from datetime import datetime as dt
import datetime
import jwt
import os

from django.shortcuts import render
from django.http import HttpResponse as res
from django.http import JsonResponse as jsonify
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .models import Question, User, Answer


def createToken(username, id):
    token = jwt.encode({
        "username": username,
        "id": id,
        "exp": dt.now() + datetime.timedelta(minutes=30)
        }, str(os.getenv('SECRET_KEY')) or 'T#1515M3', algorithm='HS256')
    return token


def jwtManager(reqFunc):
    def authWrapper(req, **kwargs):
        token = req.META.get('HTTP_AUTHORIZATION')
        if token:
            try:
                user = jwt.decode(token, str(os.getenv('SECRET_KEY')) or 'T#1515M3')
                req.user = User.objects.get(username=user["username"], id=user["id"])
                return reqFunc(req, **kwargs)
            except jwt.exceptions.InvalidSignatureError:
                return jsonify({"message": "Invalid token"})
            except jwt.exceptions.DecodeError:
                return jsonify({"message": "Not enough segments"})
            except jwt.exceptions.ExpiredSignatureError:
                return jsonify({"message": "Your session has timed out"})
        return(jsonify({"message": "We could not find your token"}))
    return authWrapper

@csrf_exempt
def signup(req):
    if req.method == 'POST':
        try:
            data = loads(req.body)
        except json.decoder.JSONDecodeError:
            return jsonify({"message": "Missing parameters"})
        if data['username'] and data['email'] and data['password']:
            user = User()
            user.username = data['username']
            user.email = data['email']
            user.password = data['password']
            user.save()
            return jsonify({"message": "User created successfully"})
        return jsonify({'message': 'missing parameters'})
    return jsonify({'message':'bad request'})


@csrf_exempt
@jwtManager
def getPostQue(req):
    if req.method == 'GET':
        ques = Question.objects.all();
        data = serializers.serialize('json', ques)
        return jsonify({"QUESTIONS": loads(data)})
    elif req.method == 'POST':
        if req.body:
            try:
                data = loads(req.body)
            except json.decoder.JSONDecodeError:
                return jsonify({"message": "Missing parameters"})
            que = Question()
            que.content = data['content']
            que.date_posted = dt.now()
            que.question_owner = req.user
            que.save()
            return jsonify({'message':'Question posted successfully'})
        return jsonify({'message': 'missing content'})
    return jsonify({'message':'bad request'})


@csrf_exempt
@jwtManager
def ansQue(req, queId):
    if req.method == 'POST':
        try:
            reqData = loads(req.body)
        except json.decoder.JSONDecodeError:
            return jsonify({"message": "Missing parameters"})
        if reqData['content']:
            try:
                ans = Answer()
                ans.content = reqData['content']
                ans.answer_owner = req.user
                ans.question_id = Question.objects.get(id=queId)
                ans.posted_on = dt.now()
                ans.save()
                return jsonify({"message": "Answer posted successfully"})
            except Question.DoesNotExist:
                return jsonify({"message": "Nothing here"})
        return jsonify({"message": "content is required"})
    return jsonify({"message": "Bad request"})


@csrf_exempt
@jwtManager
def getDelEditQue(req, queId):
    if req.method == 'GET':
        try:
            que = Question.objects.get(id=queId)
            return jsonify({
                "content": str(que.content),
                "id": int(que.id),
                "question_owner": int(que.question_owner.id),
                "date_posted": que.date_posted.strftime('%B %d, %Y')
            })
        except Question.DoesNotExist:
            return jsonify({"message":"Nothing here"})

    elif req.method == 'PUT':
        try:
            reqData = loads(req.body)
        except json.decoder.JSONDecodeError:
            return jsonify({"message": "Missing parameters"})
        if reqData['content']:
            try:
                que = Question.objects.get(id=queId)
                que.content = reqData['content']
                que.save()
                return jsonify({"message": "Question updated successfully"})
            except Question.DoesNotExist:
                return jsonify({"message": "Nothing here"})
        return jsonify({"message": "Missing content"})

    elif req.method == 'DELETE':
        try:
            que = Question.objects.get(id=queId)
            if que.question_owner == req.user:
                que.delete()
                return jsonify({"message": "question deleted successfully"})
            return jsonify({"message": "Only question owner can delete question"})
        except Question.DoesNotExist:
            return jsonify({"message": "Nothing here"})


@csrf_exempt
@jwtManager
def editDelAns(req, queId, ansId):
    if req.method == "PUT":
        try:
            reqData = loads(req.body)
        except json.decoder.JSONDecodeError:
            return jsonify({"message": "Missing parameters"})
        try:
            try:
                ans = Answer.objects.get(id=ansId)
                if ans.answer_owner == req.user:
                    ans.content = reqData['content']
                    ans.save()
                    return jsonify({"message": "Answer edited successfully"})
            except Answer.DoesNotExist:
                return jsonify({"message": "nothing here"})
            return jsonify({"message": "Only answer owner can edit answer"})
        except KeyError:
            return jsonify({"message":"content key is required"})
@csrf_exempt
def login(req):
    if req.method == 'POST':
        if req.body:
            data = loads(req.body)
            if data['email'] and data['password']:
                try:
                    user = User.objects.get(email=data['email'], password=data['password'])
                    token = createToken(user.username, user.id)
                    return jsonify({
                        "message": "User logged in successfully",
                        "token": token.decode('utf-8')
                    })
                except User.DoesNotExist:
                    return jsonify({"message": "Invalid credentials"})
            return jsonify({"message":"missing parameters"})
        return jsonify({"message":"missing parameters"})
    return jsonify({"message": "bad request"})
