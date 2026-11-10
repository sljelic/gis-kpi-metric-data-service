"""Shared CRUD helpers. The caller owns commit/rollback and session lifetime."""


class CRUDService:
    def __init__(self, session):
        self.session = session

    def delete(self, id):
        obj = self.session.get(self.model, id)
        if obj is None:
            return False
        self.session.delete(obj)
        self.session.flush()
        return True

    def _save(self, id, values):
        obj = self.session.get(self.model, id) if id is not None else None
        if obj is None:
            obj = self.model(**values)
            self.session.add(obj)
        else:
            for key, value in values.items():
                setattr(obj, key, value)
        self.session.flush()
        return obj
