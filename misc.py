def arrayNesting(nums):
    length = len(nums)
    res = 0
    visited = [False] * length
    for i in range(0, length):
        if (not visited[i]):
            n = 0
            index = i
            while visited[index] == False:
                n = n + 1
                visited[index] = True
                index = nums[index]
            
            res = max(n, res)
    return res