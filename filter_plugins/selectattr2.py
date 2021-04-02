# MIT License
#
# Copyright (c) 2020 Andre Lehmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections.abc import Iterable

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
