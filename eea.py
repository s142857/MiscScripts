import sys

try:
    x = int(sys.argv[1])
    y = int(sys.argv[2])

except:
    x = int(input("input x\n"))
    y = int(input("input y\n"))

print(r"\begin{tabular}{|p{1cm}|p{1cm}|p{1cm}||p{1cm}|}")
print(r"\hline")
print(r"x& y & r & q\\")
print(r"\hline")
print("0 & 1 & ", x, r" & - \\")
print("1 & 0 & ", y, r" & - \\")
a0 = 0 # past x column
b0 = 1 # past y column
a1 = 1 # current x column
b1 = 0 # current y column

while(y!=0):
    r = x%y
    q = int(x/y)
    x = y
    y = r
    a2 = a0 - (q*a1)
    b2 = b0 - (q*b1)
    a0 = a1
    b0 = b1
    a1 = a2
    b1 = b2
    print(a1, " & ", b1, " & ", r, " & ", q, r" \\")

print("\\hline")
print(r"\end{tabular}\\")
