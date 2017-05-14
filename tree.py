import sys

class Comment:
    def __init__(self, cid, pid, uid, url):
        self.cid = cid
        self.pid = pid
        self.uid = uid
        self.url = url

    def getNode(self):
        return HateComment(self.cid)


class HateNode:
    """Shared base node structure."""

    def __init__(self):
        self.children = []
        self.parent = None

    def addComment(self, comment):
        """
        Tries to add the given comment to this node or its children, depending
        on its parent id and stuff.
        Returns True on success, False otherwise.
        """
        return False

    def getDepth(self):
        if not self.children:
            return 1
        else:
            return 1 + max((child.getDepth() for child in self.children))

    def getNodeCount(self):
        if not self.children:
            return 1
        else:
            return 1 + sum((child.getNodeCount() for child in self.children))

    def writeCSV(self, writer):
        return

    def _linkComment(self, comment):
        """
        Adds the given node as a child node and links it properly.
        """
        if (isinstance(comment, Comment)):
            node = comment.getNode()
            self.children.append(node)
            node.parent = self

    def debugPrint(self):
        self._debugPrint(0)


class HateComment(HateNode):
    """Node that contains data pertaining to a single comment."""

    def __init__(self, cid):
        self.cid = cid
        HateNode.__init__(self)

    def addComment(self, comment):
        """Override"""
        if (self.cid == comment.pid):
            # The comment is a child of this one.
            self._linkComment(comment)
            return True
        else:
            # Check all children of this comment.
            for child in self.children:
                if (child.addComment(comment)):
                    return True
        return False

    def getCommentIDs(self):
        result = [self.cid]
        for child in self.children:
            result += child.getCommentIDs()
        return result

    def writeCSV(self, cursor, writer):
        ids = self.getCommentIDs()
        cursor.execute(
            """
            SELECT *
            FROM comments
            WHERE cid IN ({0})
            ORDER BY cid, created
            """.format(','.join([str(id) for id in ids]))
        )
        for row in cursor:
            writer.write(','.join(['"' + str(x).replace('"', '""') + '"' for x in row]) + '\n')
        return

    def _debugPrint(self, indent):
        print('-' * indent + ' ' + str(self.cid) + ' (' + str(self.getNodeCount()) + ', ' + str(self.getDepth()) + ')')
        for child in self.children:
            child._debugPrint(indent + 2)


class HateArticle(HateNode):
    """Node that contains data pertaining to a single article."""

    def __init__(self, url):
        self.url = url
        HateNode.__init__(self)

    def addComment(self, comment):
        """Override"""
        if (self.url == comment.url):
            # The comment belongs to this article.
            if (comment.pid == 0):
                self._linkComment(comment)
                return True
            else:
                for child in self.children:
                    if (child.addComment(comment)):
                        return True
        return False

    def getCommentCount(self):
        return self.getNodeCount() - 1

    def partition(self, cursor, targets, stats, writers):
        """
        Partition the article's comments into sets of arbitrary sizes.
        :param targets: Target sizes of the partitions summing up to not more than 1 (100%). Should be sorted ASC.
        :param stats: Current stats of the partitions if previous articles were already partitioned.
        :param writers: Array of writers to which the sets are written.
        """
        comments = sorted([(x.getNodeCount(), x) for x in self.children], key=lambda x: x[0])
        commentCount = self.getNodeCount()
        binSizes = [target * commentCount for target in targets]

        # Strategy:
        # - start at "largest" comment (DESC)
        # - put it in the first bin it fits into (sorted by bin size ASC)
        # - if no bin is big enough, put it into the bin that has the largest global deficit
        for comment in comments:
            bin = -1
            for i, binSize in enumerate(binSizes):
                if comment[0] < binSize:
                    bin = i
                    break
            if bin < 0:
                maxDeficit = -sys.maxint - 1;
                maxIndex = -1
                for i, target in enumerate(targets):
                    deficit = (target * sum(stats)) / stats[i]
                    if deficit > maxDeficit:
                        maxDeficit = deficit
                        maxIndex = i
            binSizes[bin] -= comment[0]
            stats[bin] += comment[0]
            comment[1].writeCSV(cursor, writers[bin])

    def writeCSV(self, cursor, writer):
        for child in self.children:
            child.writeCSV(cursor, writer)

    def _debugPrint(self, indent):
        print
        print(self.url)
        for child in self.children:
            child._debugPrint(indent + 2)