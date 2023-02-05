import numpy as np


def minEditDistance(source: str, target: str, del_cost=1, ins_cost=1, sub_cost=2, alignment=True, debug=True) -> int:
    '''
    :param source:源字符串
    :param target:目标字符串
    :param del_cost:删除代价，可以定制为具体的每个字母和代价的关系字典，也可以就是一个常量，默认为1
    :param ins_cost:插入代价，可以定制为具体的每个字母和代价的关系字典，也可以就是一个常量，默认为1
    :param sub_cost:替换代价，可以定制为具体的每对字母和代价的关系字典，也可以就是一个常量，默认为2
    :param alignment:是否输出对齐结果
    :param debug:是否输出内容
    :return:最小编辑距离
    '''

    def delcost(c):
        if isinstance(del_cost, dict):
            return del_cost[c.lower()]
        return del_cost

    def inscost(c):
        if isinstance(ins_cost, dict):
            return ins_cost[c.lower()]
        return ins_cost

    def subcost(c1, c2):
        if c1 == c2:
            return 0
        else:
            if isinstance(sub_cost, dict):
                return sub_cost[c1.lower()][c2.lower()]
            return sub_cost

    n = len(source)
    m = len(target)
    D = [[0 for i in range(m + 1)] for j in range(n + 1)]
    P = [[[] for i in range(m + 1)] for j in range(n + 1)]  # Pointers Matrix
    points = [(-1, 0), (-1, -1), (0, -1), (-1, -1)]
    D[0][0] = 0
    # 初始化
    for i in range(1, m + 1):
        D[0][i] += D[0][i - 1] + inscost(target[i - 1])
        P[0][i].append(2)
    for i in range(1, n + 1):
        D[i][0] += D[i - 1][0] + delcost(source[i - 1])
        P[0][i].append(0)
    # 递归计算
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            distances = [D[i - 1][j] + delcost(source[i - 1]),
                         D[i - 1][j - 1] + subcost(source[i - 1], target[j - 1]),
                         D[i][j - 1] + inscost(target[j - 1])]
            pos = np.argmin(distances)
            mindis = distances[pos]
            if distances[1] == mindis and source[i - 1] == target[j - 1]:
                P[i][j].append(3)
            else:
                for k in range(3):
                    if distances[k] == mindis:
                        P[i][j].append(k)
            D[i][j] = mindis
    if alignment:
        i, j = n, m
        backtrace = []
        while i > 0 or j > 0:
            backtrace.append((i, j))
            point = points[P[i][j][0]]
            i += point[0]
            j += point[1]
        backtrace.reverse()
        alignment_1 = ''
        alignment_2 = ''
        alignment_3 = ''
        for b in backtrace:
            i, j = b
            point_type = P[i][j][0]
            if point_type == 0:
                s1 = source[i - 1]
                s2 = '*'
                s3 = 'd'
            elif point_type == 1:
                s1 = source[i - 1]
                s2 = target[j - 1]
                s3 = 's'
            elif point_type == 2:
                s1 = '*'
                s2 = target[j - 1]
                s3 = 'i'
            else:
                s1 = source[i - 1]
                s2 = target[j - 1]
                s3 = ' '
            alignment_1 += s1
            alignment_2 += s2
            alignment_3 += s3
        if debug:
            print(f'alignment from {source} to {target}:\n{alignment_1}\n{alignment_2}\n{alignment_3}')
    if debug:
        print(f'min edit distance from {source} to {target} is {D[n][m]}')
    return D[n][m]


if __name__ == '__main__':
    # exercise 2.4
    minEditDistance("leda", "deal", sub_cost=1)
    # exercise 2.5
    minEditDistance("drive", "brief")
    minEditDistance("drive", "drivers")
    # example in book
    minEditDistance("execution", "intention")
