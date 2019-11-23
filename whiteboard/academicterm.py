class AcademicTerm(object):
    def __init__(self, system, system_plural, name, name_plural):
        self.system = system.lower()
        self.system_plural = system_plural.lower()
        self.name = name.lower()
        self.name_plural = name_plural.lower()

    @property
    def system_capital(self):
        return self.system.capitalize()

    @property
    def system_plural_capital(self):
        return self.system_plural.capitalize()

    @property
    def name_capital(self):
        return self.name.capitalize()

    @property
    def name_plural_capital(self):
        return self.name_plural.capitalize()
