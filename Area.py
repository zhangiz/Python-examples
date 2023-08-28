#CALCULATIN TRIANGLE AREA

# accepting values for the three sides of a triangle from the user
a = float(input('Enter first side: '))  
b = float(input('Enter second side: '))  
c = float(input('Enter third side: '))  
  
# calculate the semi-perimeter  
s = (a + b + c) / 2  
  
# calculate the area 
area = (s*(s-a)*(s-b)*(s-c)) **  0.5   
print("The area of the triangle is %0.2f" %area)   