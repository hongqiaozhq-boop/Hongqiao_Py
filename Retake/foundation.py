"""
根据输入的电数阶梯计算电费
"""
# electricity=float(input("请输入使用了多少度电："))
# if electricity < 2880:
#     print(f"你需要缴纳的电费为{electricity * 0.4883}")
#
# if 2880 <= electricity <= 4800:
#     print(f"你需要缴纳的电费为{electricity * 0.5383}")
#
# if electricity > 4800:
#     print(f"你需要缴纳的电费为{electricity * 0.7883}")


"""
根据用户输入的数字，判断该数字是奇数还是偶数
"""
# try:
#     num = int(input("请输入数字："))
#     if num % 2 == 0:
#         print("你输入的数字是偶数")
#     else:
#         print("你输入的数字是奇数")
# except Exception:
#     print("请输入int类型数字")



"""
根据用户输入的年龄,判断用户是否已经成年
"""
# try:
#     day=int(input("请输入你的年龄:"))
#     if day < 18:
#         print("你还未成年")
#     else:
#         print("你已经成年了")
# except Exception:
#     print("请输入int类型数据")


"""
根据输入的数字,判断数字是正数还是负数,不考虑0
"""
# try:
#     num=int(input("请输入一个数字:"))
#     if num == 0:
#         print("不能输入为0的数字")
#     if num > 0:
#         print("数字为正数")
#     if num < 0:
#         print("数字为负数")
# except Exception:
#     print("只能输入int类型数字")


"""
根据输入的考试分数,判断是否及格了
"""
# num=int(input("请输入你的考试分数:"))
# if num > 100 or num < 0:
#     print("你输入的成绩超出范围")
# else:
#     if num >= 60 :
#         print("你的成绩及格了")
#     else:
#         print(f"你未及格,成绩是{num}")



"""
打印出一个99乘法表
"""
# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f"{i}*{j}={i*j}",end="\t")
#     print()


"""
打印出一个等边三角形
"""

# n = 6  # 设定三角形的边长（高度）
# for i in range(1, n + 1):  # 外层循环：控制行数
#     for j in range(1, n + i):  # 内层循环：控制每行打印的字符数
#         if j <= n - i:  # 判断当前位置应该打印空格还是星号
#             print('=', end='')  # 打印空格（不换行）
#         else:
#             print('*', end='')  # 打印星号（不换行）
#     print()  # 每行结束后换行


"""
列表推导式生成一个1-20平方数的列表
"""
# list=[i**2 for i in range(1,21)]
# print(list)

# import random
# list=[]
# for i in range(1,21):
#     num=random.randint(1,21)
#     list.append(num**2)
# print(list)
#
# list=[random.randint(1,21)**2 for i in range(5)]
# print(list)


"""
将多个列表合并成一个列表并且进行去重
"""
# list1=[1,2,3,4,5,6]
# list2=[3,4,5,6,7,8]
# list3=[9,10]
#1.遍历出来放入一个列表中
# for i in list2:
#     if i not in list1:
#         list1.append(i)
# for i in list3:
#     if i not in list1:
#         list1.append(i)
# print(list1)

#2.先合并再去重--强转
# list4=list1+list2+list3
# print(list(set(list4)))



"""
提取列表中的能被3或则5整除的数字,并进行平方然后组成一个新的列表
"""
# list=[i for i in range(1,31)]
# list1=[]
# for i in list:
#     if i % 3==0 or i % 5==0:
#         list1.append(i**2)
# print(list1)


"""
提取正数并组成一个新的列表
"""
#1.遍历list的切片,小于等于0的进行删除
# list=[i for i in range(-10,10)]
# for i in list[:]:
#     if i <= 0:
#         list.remove(i)
#         print(list)
# print(list)
# #2.遍历list,大于等于0的放到list2
# list=[i for i in range(-10,10)]
# list2=[]
# for i in list:
#     if i >= 0:
#         list2.append(i)
# print(list2)


"""
计算每个学生的总分,各科平均分,然后一并输出
"""
# students=(
# ("张三",50,60,70),
# ("李四",80,75,60),
# ("王五",90,95,90),
# ("赵六",30,70,64)
# )
# num1 = 0
# num2 = 0
# num3 = 0

# for i in students:
#     achievement=0
#     num1 += i[1]
#     num2 += i[2]
#     num3 += i[3]
#     achievement = i[1]+i[2]+i[3]
#     # print(i[1],i[2],i[3])
#     print(f"{i[0]}:",achievement)
# print(f"平均成绩是:{num1/4},{num2/4},{num3/4}")
# list1=[]
# list2=[]
# list3=[]
# for i in students:
#     list1.append(i[1])
#     list2.append(i[2])
#     list3.append(i[3])
# print(list1,list2,list3)
# print("各科的最低分是:",min(list1),min(list2),min(list3))
# print("各科的最高分是:",max(list1),max(list2),max(list3))
# print("各科的平均分是:",sum(list1)/4,sum(list2)/4,sum(list3)/4,)

"""
字典常用操作
"""
# dict={"王林":98,"李沐":80,"张三":80,"李四":80,"王五":80}
# print(dict)
#
# dict["赵六"] = 66
# del dict["李沐"]
# dict["张三"] = 60
# print(dict)
# print(dict["王林"])
#
#
# for i in dict:
#     print(i)


"""
开发一个购物车系统,实现商品信息的添加,删除,修改,查询功能,使用字典结构存储数据
"""

option = {"1":"添加购物车","2":"修改购物车","3":"删除购物车","4":"查询购物车","5":"退出购物车"}
user = {"username":"admin","password":"123456"}
shopping_cart = {"剃刀":(20,50),"拖把":(30,50)}

while True:
    username = input("请输入你的账号:")
    password = input("请输入你的密码:")
    if username == user["username"] and password == user["password"]:
        print("*"*21,"登录成功","*"*21)
        break
    else:
        print("你的账号或密码错误,请重新输入")

while True:
    try:
        print("*"*20,"购物车系统","*"*20)
        for i in option.items():
            print(" "*18,i[0],i[1]," "*18)
        print("*"*50)
        user_option = input("请输入你要执行的操作:")
        print("*"*16,f"正在进行{option[user_option]}","*"*16)
    except Exception:
        print("请输入1-5的选项进行操作")

    #添加
    if user_option == "1":
        cat_name = input("请输入商品名称:")
        cat_price = int(input("请输入商品价格:"))
        cat_quantity_add = int(input("请输入商品数量:"))
        shopping_cart[cat_name] = cat_price,cat_quantity_add
        print("添加成功,你当前购物车内的商品信息分别是:")
        for i in shopping_cart:
            print(f"商品名称:{i}\t商品价格:{shopping_cart[i][0]}\t商品数量:{shopping_cart[i][1]}")
    #修改
    if user_option == "2":
        while True:
            cat_product = input("请输入你要修改的商品名称:")
            if cat_product in shopping_cart:
                cat_quantity = int(input("要修改的数量:"))
                shopping_cart[cat_product] = shopping_cart[cat_product][0],cat_quantity
                print(f"修改成功!{cat_product}的数量修改为{cat_quantity}")
                print(f"你当前的购物车信息如下:")
                for i in shopping_cart:
                    print(f"商品名称:{i}\t商品价格:{shopping_cart[i][0]}\t商品数量:{shopping_cart[i][1]}")
                break
            else:
                print("你输入的商品不在购物车内")

    #删除
    if user_option == "3":
        while True:
            for i in shopping_cart:
                print(f"你当前的购物车信息如下:商品名称:{i}\t商品价格:{shopping_cart[i][0]}\t商品数量:{shopping_cart[i][1]}")
            cat_pop = input("请输入你要删除的商品名称:")
            if cat_pop in shopping_cart:
                shopping_cart.pop(cat_pop)
                print(f"成功删除商品{cat_pop}")
                for i in shopping_cart:
                    print(f"你当前的购物车信息如下:{i}\t商品价格:{shopping_cart[i][0]}\t商品数量{shopping_cart[i][1]}")
                break
            else:
                print("你所输入的的商品不在你的购物车内")


    #查询
    if user_option == "4":
        for i in shopping_cart:
            print(f"你当前的购物车信息如下:商品名称:{i}\t商品价格:{shopping_cart[i][0]}\t商品数量:{shopping_cart[i][1]}")


    #退出
    if user_option == "5":
        break
        print("退出成功!")


"""
字典求平均数
"""
# dict={"a":90,"b":60,"c":80}
# sum = sum(dict.values())
# avg = sum / len(dict)
# print(avg)



