# content

in python, which is a OOP language, we can define a class with its methods:

```python
class rectangle:
    def __init__(self, width, length):
        self.width, self.length = width, length
    def area(self):
        return self.width * self.length
```

go is not a object-oriented language, something similar can be achieved with
struct method:

```go
type rectangle struct {
    width int
    length int
}
```

```go
func (r rectangle) area() int {
    return r.width * r.length
}
```

^func-def

after declaring `r`, we can do:

```go
fmt.printf(r.area())
```

in [[#^func-def]], `(r rectangle)` is called a `receiver`, which is just a
param that goes before function name. ^receiver

in fact, **methods are just functions** with _receiver arguments_ -> [A Tour of Go](https://go.dev/tour/methods/2)

## up

- [[struct]]

## down

- [[go-interfaces]]

## reference

- [A Tour of Go](https://go.dev/tour/methods/2)
