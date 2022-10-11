def set_digit_grid(number,color1,color2=(0,0,0)):
    """
        Return a list of 64 elements for SenseHat led display
        number must be positive and less than 100
        color1 is the color used to display the digits
        color2 is the background color
    """
    
    digits = [
    [[color1,color1,color1],[color1,color2,color1],[color1,color2,color1],[color1,color2,color1],[color1,color1,color1]],
    [[color2,color2,color1],[color2,color2,color1],[color2,color2,color1],[color2,color2,color1],[color2,color2,color1]],
    [[color1,color1,color1],[color2,color2,color1],[color1,color1,color1],[color1,color2,color2],[color1,color1,color1]],
    [[color1,color1,color1],[color2,color2,color1],[color1,color1,color1],[color2,color2,color1],[color1,color1,color1]],
    [[color1,color2,color1],[color1,color2,color1],[color1,color1,color1],[color2,color2,color1],[color2,color2,color1]],
    [[color1,color1,color1],[color1,color2,color2],[color1,color1,color1],[color2,color2,color1],[color1,color1,color1]],
    [[color1,color1,color1],[color1,color2,color2],[color1,color1,color1],[color1,color2,color1],[color1,color1,color1]],
    [[color1,color1,color1],[color2,color2,color1],[color2,color2,color1],[color2,color2,color1],[color2,color2,color1]],
    [[color1,color1,color1],[color1,color2,color1],[color1,color1,color1],[color1,color2,color1],[color1,color1,color1]],
    [[color1,color1,color1],[color1,color2,color1],[color1,color1,color1],[color2,color2,color1],[color1,color1,color1]]
    ]
    
    grid = [color2]*64

    if 0 <= number < 100:
        number = str(number).zfill(2)
        for i in range(5):
            grid[8+i*8:11+i*8] = digits[int(number[0])][i][:]            
            grid[12+i*8:15+i*8] = digits[int(number[1])][i][:]
    
    return grid

def main():
    a = 25
    grid = set_digit_grid(a,"#"," ")
    print("_______________")
    print("Test with",a)
    ch = ""
    for i in range(8):
        for j in range(8):
            ch += grid[i*8+j]
        ch += "\n"
    print(ch)
        
    a = 1
    grid = set_digit_grid(a,"#"," ")
    print("_______________")
    print("Test with",a)
    ch = ""
    for i in range(8):
        for j in range(8):
            ch += grid[i*8+j]
        ch += "\n"
    print(ch)
        
    a = 101
    grid = set_digit_grid(a,"#"," ")
    print("_______________")
    print("Test with",a)
    ch = ""
    for i in range(8):
        for j in range(8):
            ch += grid[i*8+j]
        ch += "\n"
    print(ch)

if __name__ == "__main__":
    main()
