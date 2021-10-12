from types import GeneratorType


class TestModule(object):

    def tests(self):
        return {
            'list': self.is_list,
        }

    def is_list(self, value):
        """Test if a value a list or generator type.

        Jinja2 provides the tests `iterable` and `sequence`, but those also
        match strings and dicts as well. To determine, if a value is essentially
        a list, you need to check the following:

            value is not string and value is not mapping and value is iterable

        This test is a shortcut, which allows to check for a list or generator
        simply with:

            value is list

        Args:
            value: A value, that shall be type tested

        Returns:
            bool: True, if value is of type list or generator, False otherwise.
        """
        return isinstance(value, (list, GeneratorType))
