def dfs(graph, path, end,results,w,weights): #找出从start到end的所有路径
    s = path[-1]
    if s == end: #判断是否走到指定位置
        results.append(path) #添加路径
        weights.append(w) #添加路径权重
        return
    for x in graph[ord(s) - 65]:
        if x not in path: #走过的不再走
            dfs(graph,path + [x],end,results,w + graph[ord(s) - 65][x],weights)
            #这里注意不能path.append(x)，因为path会跟着变

def search(graph, path, end):
    results = []
    w = 0
    weights = []
    dfs(graph, path, end, results,w,weights)
    a=sorted(enumerate(weights), key=lambda x:x[1]) #进行一个排序
    print(results) #输出所有路径
    print(results[a[0][0]]) #输出最短路径


Graph = [{'B':3,'C':4},
            {'A':1,'D':5},
            {'A':6,'E':2},
            {'A':2,'B':9},
            {'C':3,'D':5}]


r = search(Graph,['D'],'A')