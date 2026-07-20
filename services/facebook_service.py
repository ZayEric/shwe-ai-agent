from collections import Counter


class FacebookService:

    def __init__(self, facebook_data):

        """
        facebook_data : dict or list loaded from Facebook JSON
        """

        self.data = facebook_data

    ############################################################
    # Public
    ############################################################

    def summarize(self):

        return {

            "total_posts": self.total_posts(),

            "total_comments": self.total_comments(),

            "recent_posts": self.recent_posts(),

            "top_keywords": self.top_keywords(),

            "sample_comments": self.sample_comments()

        }

    ############################################################
    # Statistics
    ############################################################

    def total_posts(self):

        if isinstance(self.data, list):

            return len(self.data)

        return len(self.data.get("posts", []))

    def total_comments(self):

        posts = self._posts()

        total = 0

        for post in posts:

            comments = post.get("comments", [])

            total += len(comments)

        return total

    ############################################################
    # Recent Posts
    ############################################################

    def recent_posts(self, limit=5):

        posts = self._posts()

        result = []

        for post in posts[:limit]:

            result.append({

                "message": post.get("message", ""),

                "created_time": post.get("created_time"),

                "likes": post.get("likes", 0),

                "comments": len(post.get("comments", []))

            })

        return result

    ############################################################
    # Sample Comments
    ############################################################

    def sample_comments(self, limit=30):

        posts = self._posts()

        comments = []

        for post in posts:

            for c in post.get("comments", []):

                message = c.get("message", "")

                if message:

                    comments.append(message)

        return comments[:limit]

    ############################################################
    # Keyword Analysis
    ############################################################

    def top_keywords(self, top_n=20):

        stop_words = {

            "the", "is", "are", "was", "were",

            "and", "or", "to", "of", "a",

            "an", "for", "in", "on", "with",

            "at", "by", "this", "that"

        }

        words = []

        comments = self.sample_comments(limit=200)

        for comment in comments:

            for word in comment.lower().split():

                word = word.strip(".,!?():;\"'")

                if len(word) < 3:

                    continue

                if word in stop_words:

                    continue

                words.append(word)

        counter = Counter(words)

        return counter.most_common(top_n)

    ############################################################
    # Helper
    ############################################################

    def _posts(self):

        if isinstance(self.data, list):

            return self.data

        return self.data.get("posts", [])
