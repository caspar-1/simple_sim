import simpleSimCore as core


if __name__=="__main__":
    x=core.DataContainer_float()
    y=core.DataContainer_float()
    x.init([1,2,3,4,5,6,7,8,9,10])
    y.init([1,4,3,4,5,6,7,8,9,10])
    
    print(x+y)
    print(x-y+2)
    print(x*y)
    print(x/y)