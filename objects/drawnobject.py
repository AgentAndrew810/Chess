class DrawnObject:
    instances = []

    def __init__(self) -> None:
        self.instances.append(self)

    @classmethod
    def set_sizes(cls, screen_width: int, screen_height: int) -> None:
        # if the width is bigger than the ratio, use the height to calculate the width
        if screen_width >= screen_height * 21 / 18:
            height = screen_height
            width = round(height * 21 / 18)
        # otherwise use the width to calculate height
        else:
            width = screen_width
            height = round(width * 18 / 21)

        # use the height and width to calculate other sizes
        cls.padd = round(width / 21)
        cls.square_size = cls.padd * 2
        cls.board_size = cls.square_size * 9

        # calculate the x_padd and y_padd based on if the height or width was adjusted
        cls.x_padd = cls.padd + (screen_width - width) // 2
        cls.y_padd = cls.padd + (screen_height - height) // 2
        
        print("Here")

        # if instance has an update method call it
        for instance in cls.instances:
            if hasattr(instance, "update"):
                instance.update()
