# In this file, we define the classes that represent the data in our application.
# If our classes got to be too numerous, we could refactor them into separate files,
#  likely if we went this path, we would put them into a models directory rather than in the api directory.
class User:
    
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email
        self.date_joined = None

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined
        }

# This function will take a dictionary and return a User object
def create_user_from_dict( data: dict) -> User:
        return User(data['id'], data['username'], data['email'])

class Movie:

    def __init__(self, movie_id: int, title: str, genre: str, release_year: int, director: str):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.release_year = release_year
        self.director = director

    def __repr__(self):
        return f'<Movie {self.movie_id} - {self.title}>'

    # This function will return a dictionary representation of the Movie object
    # This is useful for converting the object to JSON
    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'genre': self.genre,
            'release_year': self.release_year,
            'director': self.director
        }

    # This function will take a dictionary and return a Movie object, this is useful to convert JSON to an object
    # This is a bit more complex syntax than the User and Ratings classes, this is what we call a class method
    # It is a method that is bound to the class itself rather than an object of the class
    # It doesn't require creation of a class instance, so it can be called on the class itself
    # An example of how to use it is
    # movie = Movie.from_dict(data)
    # Notice how this is different from the typical way of creating an object
    # movie = Movie(data['movie_id'], data['title'], data['genre'], data['release_year'], data['director'])
    @classmethod
    def from_dict(cls, data: dict) -> 'Movie':
        return cls(
            # Sometimes an id doesn't make sense to be in the dictionary, 
            #   so we'll use the get method to return None if it doesn't exist
            movie_id=data.get('movie_id',None),
            title=data['title'],
            genre=data['genre'],
            release_year=data['release_year'],
            director=data['director']
        )


class Rating:

    def __init__(
        self,
        rating_id: int,
        user_id: int,
        movie_id: int,
        rating: int,
        review: str,
        date: str,
    ):
        self.rating_id = rating_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.review = review
        self.date = date

    def __repr__(self):
        return f"<Rating {self.rating_id}>"

    def to_dict(self):
        return {
            "rating_id": self.rating_id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "rating": self.rating,
            "review": self.review,
            "date": self.date,
        }

    # This function will take a dictionary and return a Rating object
    # See the advanced_concepts documenation for more information on class methods
    # NOTE: This is the same as the create_rating_from_dict function
    @classmethod
    def from_dict(cls, data: dict) -> 'Rating':
        return cls(
            rating_id=data["rating_id"],
            user_id=data["user_id"],
            movie_id=data["movie_id"],
            rating=data["rating"],
            review=data["review"],
            date=data["date"],
        )

# This function will take a dictionary and return a Rating object
def create_rating_from_dict(data: dict) -> Rating:
    return Rating(
        data["rating_id"],
        data["user_id"],
        data["movie_id"],
        data["rating"],
        data["review"],
        data["date"],
    )
