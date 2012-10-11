class Parameters:
    def __init__(self):
        # double line break parameters
        self.double_line_break_score = 20

        # title parameters
        self.title_score_threshold = 7
        self.strict_title_points = 10
        self.first_inline_title_points = 7
        self.any_inline_title_points = 1

        # list parameters
        self.minimum_list_length = 2
        self.list_spacing = 2
        self.list_length_weight = 2

        # penalities for collisions of different block attributes
        self.list_url_collision_penalty = 10

