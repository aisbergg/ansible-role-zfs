from collections import Iterable

from ansible import errors
from jinja2.filters import environmentfilter
from jinja2.runtime import Undefined


class FilterModule(object):

    def filters(self):
        return {"selectattr2": self.selectattr2}

    @environmentfilter
    def selectattr2(self, environment, seq, attr, func_name, *args, **kwargs):
        """Filter a sequence of objects by applying a test to the specified
        attribute of each object, and only selecting the objects with the test
        succeeding.

        The filter works much like the 'selectattr', but it does not fail in
        case an attribute doesn't exists. In case an attribute is missing, a
        default value is used. The default value can be specified as a
        keyed-arg.

        Args:
            seq (Iterable): The sequence to be filtered.
            attr (str): The attribute used for filtering.
            func_name (str): The name of filter function.

        Raises:
            errors.AnsibleFilterError: Raised if 'seq' is not an iterable and
            doesn't contain a mapping.

        Yields:
            The next item of the sequence, that passes the test.

        Examples:
            {{ users | selectattr2('state', '==', 'present', default='present') | list }}
        """
        if not isinstance(seq, Iterable):
            raise errors.AnsibleFilterError("'{}' is not an iterable".format(seq))

        default = kwargs.pop('default', Undefined())
        attr = [int(x) if x.isdigit() else x for x in attr.split(".")]

        def func(item):
            if not isinstance(item, dict):
                raise errors.AnsibleFilterError("'{}' is not a mapping".format(item))

            for part in attr:
                item = environment.getitem(item, part)
                if isinstance(item, Undefined):
                    item = default
                    break

            return environment.call_test(func_name, item, args, kwargs)

        if seq:
            for item in seq:
                if func(item):
                    yield item
