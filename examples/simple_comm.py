"""
This is a simple example of how communication across clients works in
cloudviz.

We create simple client and subset classes. When a client receives a
relevant message from the hub, it just gives a summary of that
message.
"""
from cloudviz import Client, Subset, Hub, Data


class SimpleClient(Client):
    """A simple client for demonstration purposes.

    This client simply prints an informational message
    whenever it receives a message from the hub relevant to
    the data it is associated with
    """

    def __init__(self, data, name="SimpleClient"):
        Client.__init__(self, data)
        self.name = name

    def __str__(self):
        return self.name

    def update_subset(self, subset, attr=None, new=False, delete=False):
        if (subset.data != self.data):
            return
        Client.update_subset(self, subset, attr=attr,
                             new=new,
                             delete=delete)

    def _add_subset(self, subset):
        print "Client is %s\n    Added a subset: %s" % (self, subset)

    def _delete_subset(self, subset):
        print "Client is %s\n    Deleted subset: %s" % (self, subset)

    def _refresh_subset(self, subset, attr):
        print ("Client is %s\n    Modified a subset: %s\n    "
               "Changed attribute %s" % (self, subset, attr))


class SimpleSubset(Subset):
    """A simple subset with a name."""

    def __init__(self, data, name="SimpleSubset"):
        self.name = name
        # call superclass after setting self.name, to prevent the hub from
        # relaying the message
        Subset.__init__(self, data)

    def __str__(self):
        return self.name


def run_tests():
    """ A simple test suite.

    >>> run_tests()
        Client is C1
            Modified a subset: S1
            Changed attribute modification1
        Client is C1
            Added a subset: S2
        Client is C2
            Added a subset: S2
        Client is C1
            Modified a subset: S2
            Changed attribute modification2
        Client is C2
            Modified a subset: S2
            Changed attribute modification2
        Client is C3
            Added a subset: S3
        Client is C1
            Modified a subset: S1
            Changed attribute modification3
        Client is C2
            Modified a subset: S1
            Changed attribute modification3
        Client is C1
            Modified a subset: S1
            Changed attribute modification4
    """

    d = Data()
    h = Hub()
    c1 = SimpleClient(d, name="C1")
    c2 = SimpleClient(d, name='C2')
    s1 = SimpleSubset(d)
    s1.name = 'S1'

    # Test modification with single client
    h.add_client(c1)
    s1.modification1 = 1

    # Test creation and modification with 2 clients
    h.add_client(c2)
    s2 = SimpleSubset(d, name="S2")
    s2.modification2 = 1

    # Test independent data + clients
    d2 = Data()
    c3 = SimpleClient(d2, name="C3")
    h.add_client(c3)

    s3 = SimpleSubset(d2, name="S3")
    s1.modification3 = 1

    # Test client removal
    h.remove_client(c2)
    s1.modification4 = 1

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)