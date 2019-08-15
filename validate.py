def white_list(var,args):
    #this is a convienence function to take an array of values and a var
    #and runs or logic as if it were var == arg[1] or var == arg[2] or var == arg[3], can be thought of as a white list

    #cycle through args to see if ANY of its values equal our variable, return true if they do
    #return false otherwise
    for i in range(0,len(args)):
        if var == args[i]:
            return True
    return False
def safe_int(string,white=[]):
    #this is a simple program that returns none if the user supplies an invalid intager
    #string is the string to turn into an intager and white is a whitelist array of valid data to let through
    if white_list(string,white):
        #return the string if it is data that we choose to allow    
        return string
    try:
        return int(string)
    except:
        return None
def safe_float(string,white=[]):
    #this is a simple program that returns none if the user supplies an invalid intager
    #string is the string to turn into an intager and white is a whitelist array of valid data to let through
    if white_list(string,white):
        #return the string if it is data that we choose to allow
        return string
    try:
        return float(string)
    except:
        return None

