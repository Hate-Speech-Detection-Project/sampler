import sys
import psycopg2
import time
import os
import errno

import tree

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Connect to the database.
try:
    conn = psycopg2.connect("dbname='hatespeech' user='postgres' host='localhost' password='admin'")
except:
    print("Cannot connect to database.")
    sys.exit(0)

# Get list of articles from the DB.
cur = conn.cursor()
cur.execute(
    """
    SELECT DISTINCT ON (url)
           url
    FROM comments
    """
)
articles = dict([(row[0], tree.HateArticle(row[0])) for row in cur])

# Get the comments, without some of the clutter like text.
cur = conn.cursor()
cur.execute(
    """
    SELECT DISTINCT ON (cid)
           cid, pid, uid, url
    FROM comments
    ORDER BY cid ASC, pid ASC, created ASC
    """
)

print("Number of comments before tree structuring: ", cur.rowcount)

# Transform the comments into a tree structure. Dangling comments (which are answers to another
# comment which is not in the data set) are discarded.
for row in cur:
    article = articles.get(row[3])
    if article != None:
        comment = tree.Comment(row[0], row[1], row[2], row[3])
        article.addComment(comment)

commentCount = sum([article.getCommentCount() for url, article in articles.items()])
print("Number of comments after tree structuring:  ", commentCount)

# Partition the data into three sets (20%, 20%, 60%)
make_sure_path_exists('../output')
stats = [1, 1, 1]
files = [open('../output/part1.csv', 'w+'), open('../output/part2.csv', 'w+'), open('../output/part3.csv', 'w+')]
targets = [.2, .2, .6]
cursor = conn.cursor()
start = time.time()
for url, article in articles.items():
    article.partition(cursor, targets, stats, files)

print("Target partitioning was ", [int(commentCount * target) for target in targets])
print("Actual partitioning is  ", stats)
print("Partitioned comments in %s seconds" % (time.time() - start))

# pickle.dump(articles, open("save.p", "wb"))
# loaded = pickle.load(open("save.p", "rb"))
