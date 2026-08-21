"""
函数
"""
# user_name = "admin"
# user_password = "123456"
# def login(name,password):
#     if name == user_name and password == user_password:
#         return "登录成功"
#     else:
#         return "登录失败"
#
# ase=login("admin","1234567")
# print(ase)




"""
定义一个函数,根据传入的底和高计算三角形面积
"""

# def area(bottom,tall):
#     if not isinstance(bottom,(int,float)) or isinstance(bottom,bool):
#         return "底必须是数字"
#
#     if not isinstance(tall,(int,float)) or isinstance(tall,bool):
#         return "高必须是数字"
#
#     triangle_area = bottom * tall / 2
#     return triangle_area
#
#
# print(area(5, 6))




"""
定义一个函数,计算传入的字符串中元音字母的个数  aeiouAEIOU
"""

# def vowel_len(strs):
#     list = []
#     list_vowel = ["a","e","i","o","u","A","E","I","O","U"]
#     for i in strs:
#         if i in list_vowel:
#             list.append(i)
#     len_vo = len(list)
#     return len_vo
#
# print(f"你输入的字符串中元音字母的个数是:{vowel_len('fxawsetfazsd123456uiyAEIII')}")



"""
定义一个函数,传入学生高考成绩并计算其中最高分最低分和平均分
"""

# def grade(*args):
#     list = []
#     for i in args:
#         list.append(i)
#     min_fonction = min(list)
#     max_fonction = max(list)
#     avg_fonction = sum(list)/len(list)
#     return min_fonction,max_fonction,avg_fonction
#
# min_grade,max_grade,avg_grade = grade(80,90,60)
# print(f"最高分是{max_grade},最低分是{min_grade},平均分是{avg_grade}")



"""
传入底和高计算三角形面积的函数
"""
# def triangle(d,h):
#     area = (d * h) / 2
#     return area
#
# tare = triangle(5,6)
#
# print(tare)



#
# add = lambda x,y : x + y
# print(add(5, 10))

"""
列表按照字符位数排序
"""
# care_list=["a","asd","aghqsad","as","n","a","ewt","ytwry"]
# care_list.sort(key=lambda hars : len(hars),reverse=True)
# print(care_list)


"""
计算传入数据的乘阶,递归
"""
# def num(i):
#     if i == 1:
#         return 1
#     else:
#         return i * num(i - 1)
#
#
# print(num(15))





"""
定义一个用于根据传入的一批商品信息(商品名称,价格,数量),优惠(优惠券,积分),运费信息计算订单总金额的函数
1.商品优惠券需要商品金额满5000才能使用,且优惠券金额不能超过商品总金额
2.积分抵扣需要商品金额满3000才能使用,切积分抵扣不能超过商品总金额,100积分=1元
"""

# def order(*args,coupon,points,freight):
#     #计算商品总金额:商品数量*商品价格然后进行累加
#     #订单总金额 = 商品总金额 - 优惠券 - 积分/100 + 运费
#     price_list = [i[1] * i[2] for i in args]
#     total = sum(price_list)
#
#     if total >= 5000 and (coupon + points // 100) < total:
#         total = total - (coupon + points // 100) + freight
#     if 5000 < total >= 3000 and points // 100 < total:
#         total = total - points // 100 + freight
#     if total < 3000:
#         total = total + freight
#     return total
#
# Total_Price = order(("手机",200,5),("电脑",500,5),("平板",300,2),coupon=500,points=3000,freight=10)
# print(Total_Price)




# from random import choice
# list = [1,2,3,4,5,6,7,8,9]
# rd = choice(list)
# print(rd)