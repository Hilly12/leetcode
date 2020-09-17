
# 0-1 knapsack recursive
def knapsack(wvs, capacity):
    maxval = 0
    for w, v in wvs:
        if (w <= capacity):
            maxval = max(v + knapsack(list(filter(lambda wv: wv[0] != w or wv[1] != v, wvs)), capacity - w), maxval)

    return maxval