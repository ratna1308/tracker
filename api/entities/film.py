class Film:
    def __init__(
        self,
        *,
        film_id: str,
        title: str,
        description: str,
        release_year: int,
        watched: bool = False
    ):
        """
        Parameters
        ----------
        film_id: str
            The film UUID represented by a string.
        title: str
            The film title.
        description: str
            The film description.
        release_year: int
            The release year of the film.
        watched: bool
            Boolean that indicates if the film has been watched.

        Return
        ------
        None
            This function doesn't return anything.

        Raises
        ------
        ValueError
             Raised when film_id is null.
        """
        if film_id is None:
            raise ValueError("Film id is required!")
        self._id = film_id
        self._title = title
        self._description = description
        self._release_year = release_year
        self._watched = watched

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def release_year(self) -> int:
        return self._release_year

    @property
    def watched(self) -> bool:
        return self._watched

    def __eq__(self, o: object) -> bool:
        """
        NOTE :
        We are overriding equals method as absolute object comparison can fail
        because each object of a class is a new object and will have a different
        `id()`.

        Args:
            o:

        Returns:

        """

        if not isinstance(o, Film):
            return False
        return (
            self.id == o.id
            and self.title == o.title
            and self.description == o.description
            and self.release_year == o.release_year
            and self.watched == o.watched
        )


if __name__ == "__main__":
    # NOTE
    # This is added for understanding.

    film = Film(
        film_id="random film_id",
        title="random title",
        description="random description",
        release_year="random release year",
        watched=True,
    )
