from functools import wraps

_property = property

# NOTE: dependent properties should come AFTER all the 'indep' properties
# NOTE: caches are based on property names, so re-using names will probably
# break things. changing cachename to be based on id() would eliminate those
# errors but make the resulting properties less readable.

def clear_cached_properties(obj,tag=None):
    names = [d.fget.__name__ for d in obj.__class__.__dict__.itervalues()
                if isinstance(d,cachedproperty) and (tag is None or tag in d.tags)]
    for name in names:
        del obj.__dict__['__cachedprop_%s' % name]

class property(_property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self._dependents = []
        super(property,self).__init__(fget,self._wrap_setter(fset),fdel,doc)

    def _wrap_setter(self,fset):
        if fset is None:
            return None
        else:
            @wraps(fset)
            def wrapped(instance,*args):
                for dp in self._dependents:
                    cachename = '__cachedprop_%s' % dp.fget.__name__
                    if hasattr(instance,cachename):
                        del instance.__dict__[cachename]
                return fset(instance,*args)
            return wrapped

class cachedproperty(property):
    def __init__(self,*depends_on):
        self.tags = []
        for prop in depends_on:
            assert isinstance(prop,(property,str))
            if isinstance(prop,property):
                prop._dependents.append(self)
            else:
                self.tags.append(prop)
        super(cachedproperty,self).__init__()

    def __call__(self,f):
        super(cachedproperty,self).__init__(fget=self._wrap_getter(f))
        return self

    def _wrap_getter(self,fget):
        @wraps(fget)
        def wrapped(instance,*args):
            cachename = '__cachedprop_%s' % self.fget.__name__
            if not hasattr(instance,cachename):
                instance.__dict__[cachename] = fget(instance,*args)
            return instance.__dict__[cachename]
        return wrapped

###

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


