# Data Model
The data model for the movie review system is shown below. The system has three tables: `USER`, `MOVIE`, and `RATING`. The `USER` table stores information about the users of the system. The `MOVIE` table stores information about the movies in the system. The `RATING` table stores information about the ratings and reviews of the movies by the users.

```markdown
```mermaid
erDiagram
    USER {
        int id
        string username
        string email
    }
    MOVIE {
        int id
        string title
        string genre
        date release_date
    }
    RATING {
        int id
        int user_id
        int movie_id
        int rating
        string review
        date date
    }
    USER ||--o{ RATING : gives
    MOVIE ||--o{ RATING : receives
```