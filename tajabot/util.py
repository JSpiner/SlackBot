

def getEditDistance(str1, str2):

    d = [[0 for col in range(len(str2) + 1)] for row in range(len(str1) + 1)]

    print(str1)
    print(str2)
    for i in range(0, len(str1) + 1):
        d[i][0]= i
    
    for i in range(0, len(str2) + 1):
        d[0][i] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min([d[i-1][j-1] + 1, d[i][j-1] + 1, d[i-1][j] + 1])
    
    return d[len(str1)][len(str2)]
