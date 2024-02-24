class Move:
    def __init__(
        self, old_rank: int, old_file: int, new_rank: int, new_file: int
    ) -> None:
        self.old_rank = old_rank
        self.old_file = old_file
        self.new_rank = new_rank
        self.new_file = new_file

    @property
    def old_pos(self) -> tuple[int, int]:
        return (self.old_rank, self.old_file)

    @property
    def new_pos(self) -> tuple[int, int]:
        return (self.new_rank, self.new_file)
