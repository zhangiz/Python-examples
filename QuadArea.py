
# accepting values for the heights of the triangles from the user
h1 = float(input('Enter first height: '))  
h2 = float(input('Enter second height: '))  

# accepting values for the diagonal  from the user
d = float(input('Enter the diagonal: '))  

  
# calculate the area 
area = 0.5 * d * (h1+h2) 

print("The area of the triangle is %0.2f" %area)   