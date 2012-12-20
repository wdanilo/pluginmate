def unchanged(func):
    "This decorator doesn't add any behavior"
    return func

def disabled(func):
    "This decorator disables the provided function, and does nothing"
    def empty_func(*args,**kargs):
        pass
    return empty_func

# define this as equivalent to unchanged, for nice symmetry with disabled
enabled = unchanged