class Sun:
    n = 0  # number of instances of this class

    def __new__(cls):
        if cls.n == 0: 
            cls.n += 1
            return object.__new__(cls)  # create new object of the class
        
sun1 = Sun()
sun2 = Sun()

print(sun1)  # <__main__.Sun object at 0x1106884a8>
print(sun2)  # None