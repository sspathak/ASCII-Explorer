def reader(values):
    f=open("level1.txt", "r")
    # N=no. of lines
    #x = the position from which the substring must begin
    x=values[0]
    x-=1
    #y=the position at which the substring should end
    list1=[]
    for line in range(values[2]):
        j=f.readline()
        t=j[values[0]:values[1]]
        list1.append(t)
    return list1

    
