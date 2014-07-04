class A(object):
    def __init__(self,x):
        self.x = x

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,val):
        self._x = val

a = A(5)
print a.x
a.x = 6
print a.x

print

class B(object):
    def __init__(self,x):
        self.x = x

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,val):
        self._x = val

    @cachedproperty(x,'foo')
    def y(self):
        print 'computing y!'
        return self.x*2

b = B(5)
print b.x
print b.y
print b.y
print

b.x = 7
print b.y
print b.y
print

b2 = B(5)
print b.y
b2.x = 10
print b.y
print b2.y
print

print b.y
clear_cached_properties(b,'foo')
print b.y
print

print b.y
clear_cached_properties(b,'bar')
print b.y
print

