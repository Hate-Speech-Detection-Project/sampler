import sys
import psycopg2
import time

import tree

# Connect to the database.
try:
    conn = psycopg2.connect("dbname='hatespeech' user='postgres' host='localhost' password='admin'")
except:
    print "Cannot connect to database."
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
articles = [tree.HateArticle(row[0]) for row in cur]

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

print "Number of comments before tree structuring: ", cur.rowcount

# Transform the comments into a tree structure. Dangling comments (which are answers to another
# comment which is not in the data set) are discarded.
for row in cur:
    comment = tree.Comment(row[0], row[1], row[2], row[3])
    for article in articles:
        if article.addComment(comment):
            break

commentCount = sum([article.getCommentCount() for article in articles])
print "Number of comments after tree structuring:  ", commentCount

# Partition the data into three sets (20%, 20%, 60%)
stats = [0, 0, 0]
files = [open('output/part1.csv', 'w'), open('output/part2.csv', 'w'), open('output/part3.csv', 'w')]
targets = [.2, .2, .6]
cursor = conn.cursor()
start = time.time()
for article in articles:
    article.partition(cursor, targets, stats, files)

print "Target partitioning was ", [int(commentCount * target) for target in targets]
print "Actual partitioning is  ", stats
print "Partitioned comments in %s seconds" % (time.time() - start)

# pickle.dump(articles, open("save.p", "wb"))
# loaded = pickle.load(open("save.p", "rb"))
