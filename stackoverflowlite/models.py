from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    '''Define users table
    '''
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=32)


class Question(models.Model):
    '''Define questions table
    '''
    content = models.TextField()
    date_posted = models.DateTimeField('date_posted')
    question_owner = models.ForeignKey(User, on_delete='CASCADE')

    def __str__(self):
        return(self.content)


class Answer(models.Model):
    '''Define answers table
    '''
    content = models.TextField()
    answer_owner = models.ForeignKey(User, on_delete='CASCADE')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    question_id = models.ForeignKey(Question, on_delete='CASCADE')
    posted_on = models.DateTimeField()

    def __str__(self):
        return(self.content)


class Vote(models.Model):
    '''define votes table
    '''
    answer_id = models.ForeignKey(Answer, on_delete='CASCADE')
    voter = models.ForeignKey(User, on_delete='CASCADE')
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def __str__(self):
        return(self.answer_id)
