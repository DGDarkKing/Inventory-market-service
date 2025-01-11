from conditions.interfaces.base_specification import SqlAlchemySpecification


class EmptyCondition(SqlAlchemySpecification):
    def __init__(self):
        super().__init__(None)
