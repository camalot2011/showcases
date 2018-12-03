from lxml import html,etree
from datetime import datetime
import os

def localpath(path):
    return 'file://' + os.path.join(os.path.abspath(os.path.curdir), path)

def get_avg(val):
    '''take in key,upvote_count,downvote_count
       return key, up/(up+down)'''
    if (val[1] is None) and (val[2] is None):
        return (val[0], None) #None for None on both "up" and "down"
    elif val[1] is None and (val[2] is not None):
        return (val[0], 0) #0 for None on "up" but not in "down"
    elif (val[1] is not None) and (val[2] is None):
        return (val[0], 1) #1 for None in "down"
    else:
        return (val[0], val[1]/(val[1]+val[2]))
    
def bool_to_int(val):
    return 1 if val else 0

def add_two(val1,val2):
    return (val1[0]+val2[0],val1[1]+val2[1])

class Vote(object):
    '''Vote class for parsing the posts from
       AllPosts comments'''
    
    def __init__(self, Id, postid, votetypeid, creationdate,
                       userid, bountyamount):
        self.Id = Id
        self.postid = postid
        self.votetypeid = votetypeid
        self.creationdate = creationdate
        self.userid = userid
        self.bountyamount = bountyamount
        
    @classmethod
    def parse(cls, line):
        tree = html.fromstring(line)
        Id = tree.attrib.get('id','0')
        postid = tree.attrib.get('postid','0')
        votetypeid = int(tree.attrib.get('votetypeid',0)) 
        creationdate = datetime.strptime(tree.attrib.get('creationdate'),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        userid = tree.attrib.get('userid','0')
        bountyamount = int(tree.attrib.get('bountyamount',0))
        
        
        return cls(Id, postid, votetypeid, creationdate,
                   userid, bountyamount)
    
class User(object):
    '''User class for parsing the users from
       AllUsers comments'''
    
    def __init__(self, Id, reputation, creationdate, displayname,
                   emailhash, lastaccessdate, websiteurl,
                   location, age, aboutme, views, upvotes, downvotes):
        self.Id = Id
        self.reputation = reputation
        self.creationdate = creationdate
        self.displayname = displayname
        self.emailhash = emailhash
        self.lastaccessdate = lastaccessdate
        self.websiteurl = websiteurl
        self.location = location
        self.age = age
        self.aboutme = aboutme
        self.views = views
        self.upvotes = upvotes
        self.downvotes = downvotes
        
    @classmethod
    def parse(cls, line):
        tree = html.fromstring(line)
        Id = int(tree.attrib.get('id','0'))
        reputation = int(tree.attrib.get('reputation','0'))
        creationdate = datetime.strptime(tree.attrib.get('creationdate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        displayname = tree.attrib.get('displayname','')
        emailhash = tree.attrib.get('emailhash','')
        lastaccessdate = datetime.strptime(tree.attrib.get('lastaccessdate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        websiteurl = tree.attrib.get('websiteurl','')
        location = tree.attrib.get('location','')
        age = int(tree.attrib.get('age','0'))
        aboutme = tree.attrib.get('aboutme','')
        views = tree.attrib.get('views','')
        upvotes = tree.attrib.get('upvotes','')
        downvotes = tree.attrib.get('downvotes','')
        
        return cls(Id, reputation, creationdate, displayname,
                   emailhash, lastaccessdate, websiteurl,
                   location, age, aboutme, views, upvotes, downvotes)
    
class Post(object):
    '''Post class for parsing the posts from
       AllPosts comments'''
    
    def __init__(self, Id, posttypeid, parentid, acceptedanswerid, 
                 creationdate, score, viewcount, body, owneruserid,
                 lasteditoruserid, lasteditordisplayname, lasteditdate, 
                 lastactivitydate, communityowneddate, closeddate, 
                 title, tags, answercount, commentcount, favoritecount, 
                 paragraph):
        self.Id = Id
        self.posttypeid = posttypeid
        self.parentid = parentid
        self.acceptedanswerid = acceptedanswerid
        self.creationdate = creationdate
        self.score = score
        self.viewcount = viewcount
        self.body = body
        self.owneruserid = owneruserid
        self.lasteditoruserid = lasteditoruserid
        self.lasteditordisplayname = lasteditordisplayname
        self.lasteditdate = lasteditdate
        self.lastactivitydate = lastactivitydate
        self.communityowneddate = communityowneddate
        self.closeddate = closeddate
        self.title = title
        self.tags = tags
        self.answercount = answercount
        self.commentcount = commentcount
        self.favoritecount = favoritecount
        self.paragraph = paragraph
        
    @classmethod
    def parse(cls, line):
        tree = html.fromstring(line)
        Id = int(tree.attrib.get('id','0'))
        posttypeid = int(tree.attrib.get('posttypeid',0))
        parentid = tree.attrib.get('parentid','0')
        acceptedanswerid = int(tree.attrib.get('acceptedanswerid',-1))
        creationdate = datetime.strptime(tree.attrib.get('creationdate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        score = int(tree.attrib.get('score',0))
        viewcount = int(tree.attrib.get('viewcount','0'))
        body = tree.attrib.get('body','')
        owneruserid = int(tree.attrib.get('owneruserid','0'))
        lasteditoruserid = tree.attrib.get('lasteditoruserid','0')
        lasteditordisplayname = tree.attrib.get('lasteditordisplayname','')
        lasteditdate = datetime.strptime(tree.attrib.get('lasteditdate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        lastactivitydate = datetime.strptime(tree.attrib.get('lastactivitydate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        communityowneddate = datetime.strptime(tree.attrib.get('communityowneddate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        closeddate = datetime.strptime(tree.attrib.get('closeddate',
                                         "2030-03-05T22:28:34.823"),
                                         '%Y-%m-%dT%H:%M:%S.%f')
        title = tree.attrib.get('title','')
        tags = tree.attrib.get('tags','')
        answercount = int(tree.attrib.get('answercount',0)) 
        commentcount = int(tree.attrib.get('commentcount',0))
        favoritecount = int(tree.attrib.get('favoritecount',0))
        paragraph = ''
        if (len(body) > 0) and ('<p' in body) and ('/p>' in body):
            tree_body = html.fromstring(body)
            if len(tree_body) > 0:
                paragraph = tree_body.findall('p')
                if len(paragraph) > 0:
                    paragraph = [p.text_content() for p in paragraph]
                    paragraph = ' '.join(paragraph)
        
        return cls(Id, posttypeid, parentid, acceptedanswerid, 
                 creationdate, score, viewcount, body, owneruserid,
                 lasteditoruserid, lasteditordisplayname, lasteditdate, 
                 lastactivitydate, communityowneddate, closeddate, 
                 title, tags, answercount, commentcount, favoritecount, 
                 paragraph)