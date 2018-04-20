from django.db import models
from django.contrib.auth.models import User

# a dictionary
# there are multiple dictionarys in the service, such as CET4, CET6, tofel, GRE, etc.
class Dict(models.Model):
    title = models.CharField(max_length=30)     # the title of the dictionary
    word_count = models.IntegerField()          # how many words does it contain
    description = models.CharField(max_length=100)      # short description of this dictionary
    cover_image = models.ImageField()           # cover image of this dictionary

# a word in a dictionary
class Word(models.Model):
    dict_id = models.ForeignKey('Dict', on_delete=models.CASCADE)       # which dictionary does it belongs to
    word = models.CharField(max_length=100)     # the word
    translation = models.CharField(max_length=100)      # its meaning in Chinese

# a word adde by user
class CustomWord(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)       # who added this word
    word = models.CharField(max_length=100)     # the word
    translation = models.CharField(max_length=100)      # its meaning in Chinese

# learning progress of a user with a word
class Progress(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)       # who learn this word
    word = models.CharField(max_length=100)     # the word
    familiarity = models.PositiveSmallIntegerField()        # how familiar is the user with the word
    '''
    Familiarity varies from 0 to 6. It is generated automatically by recording how long 
    does it take for the user to response to this word. We assume that the faster he/she responses, 
    the more familiar he/she is with the word, which will lead to a higher value in familiarity.
    0 means the user is totally new to this word, and 5 mean the user is extremely familiar with it.
    6 means the user thinks this word is too simple for him/her and doesn't want it to appear again.
    We will reduce the frequence of appearing of those words which possess high score in familiarity.
    '''
    reinforce_cycle = models.PositiveSmallIntegerField()        # which reinforcement cycle is the user in
    reinforce_date = models.DateField()     # the previous reinforce date
    '''
    It takes 5 reinforcement cycle for a user to get extremely familiar with a word, according to 
    Hermann Ebbinghaus. To be more specifically, a word will appear in the first day, second day, 
    third day, fifth day and seventh day. $reinforce_cycle indicates which cycle is the user currently in,
    and $reinforce_date indicates the last appearing date of this word. With these two variables, we can 
    determine when should this word appear again.
    '''
