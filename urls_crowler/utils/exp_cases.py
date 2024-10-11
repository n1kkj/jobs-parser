class ExpCases:
    INTERN = ('intern', 0)
    JUNIOR = ('junior', 1)
    MIDDLE = ('middle', 2)
    SENIOR = ('senior', 3)
    LEAD = ('lead', 4)
    NONE = ('', None)

    @classmethod
    def get_exp(cls, exp):
        if exp.lower() == cls.INTERN[0]:
            return cls.INTERN[1]
        elif exp.lower() == cls.JUNIOR[0]:
            return cls.JUNIOR[1]
        elif exp.lower() == cls.MIDDLE[0]:
            return cls.MIDDLE[1]
        elif exp.lower() == cls.SENIOR[0]:
            return cls.SENIOR[1]
        elif exp.lower() == cls.LEAD[0]:
            return cls.LEAD[1]
        return exp
