from base.choices import StateStatuses


class BaseDbIO:
    model = None

    @property
    def model(self):
        """Define the model property."""
        return self.model

    def get_obj(self, kwargs):
        """This method is used to get the database object."""
        return self.model.objects.get(**kwargs)

    def create_obj(self, kwargs):
        """Save/create instances of ORM into the database."""
        return self.model.objects.create(**kwargs)

    def update_obj(self, model_obj, kwargs):
        """Update the ORM instance."""
        for key, value in kwargs.items():
            setattr(model_obj, key, value)
        model_obj.save()
        return model_obj

    def filter_obj(self, kwargs):
        data = self.model.objects
        for key, value in kwargs.items():
            data = data.filter(**{key: value})
        return data

    def filter_active_obj(self, kwargs):
        data = self.model.objects
        for key, value in kwargs.items():
            data = data.filter(**{key: value})
        data = data.filter(state=StateStatuses.ACTIVE)
        return data

    def get_all(self):
        return self.model.objects.all()

    def get_all_active(self):
        return self.model.objects.filter(state=StateStatuses.ACTIVE)

    def get_or_create_object(self, kwargs):
        return self.model.objects.get_or_create(**kwargs)

    def delete_obj(self, kwargs):
        """This method is used to get the database object."""
        return self.get_obj(kwargs).delete()

    def delete_with_filter_obj(self, kwargs):
        """This method is used to get the database object."""
        return self.filter_obj(kwargs).delete()

    def update_or_create(self, kwargs):
        """Update/create instances of ORM into the database."""
        return self.model.objects.update_or_create(**kwargs)
