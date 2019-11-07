class CampusCard(object):
    def __init__(self, formal_name, min_len, max_len):
        assert 1 <= min_len <= max_len

        self.formal_name = formal_name
        self.min_len = min_len
        self.max_len = max_len

    def __str__(self):
        return '{}{}-Character {}'.format(f"{self.min_len}- to " if self.min_len < self.max_len else '', self.max_len, self.formal_name)
