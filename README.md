This code is an experiment in making cached properties which can depend on other
properties. The idea is to make something like this:

```python
from cachedproperties import property, cachedproperty

class A(object):
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,val):
        self._x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,val):
        self._y = val

    # z is cached and depends on the value of x and y
    @cachedproperty(x,y)
    def z(self):
        return expensive_computation(self.x,self.y)
```

The value of `z` is a pure function of the value of `x` and `y`, so it needs to
be recomputed when `x` or `y` changes. However, if `z` is expensive to compute,
it'd be nice to cache the value and only recompute it when necessary. The
`@cachedproperty(x,y)` decorator takes care of that bookkeeping.

Cached properties can also be tagged with strings, as in

```python
from cachedproperties import property, cachedproperty, \
        clear_cached_properties

class A(object):
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self,val):
        self._x = val

    @cachedproperty(x,'foo')
    def y(self):
        return expensive_computation(self.x)

a = A()
```

The cache can be cleared by calling `clear_cached_properties` on the instance.
For example,

```python
clear_cached_properties(a,tag='foo')
```

clears all cachedproperties on `a` tagged with 'foo'. Without specifying a tag,
all caches are cleared.

This code is probably totally broken, though...

