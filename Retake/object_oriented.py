# class Pen:
#     def __init__(self,type,brand,color,price):
#         self.type = type
#         self.price = price
#         self.brand = brand
#         self.color = color
#
#     def pen_buy(self,quantity):
#         total = self.price * quantity
#         return total
#
#     @staticmethod
#     def pen_sum(*args):
#         price_sum = sum(args)
#         return price_sum
#
#
# p1 = Pen("钢笔","橙光","红色",20)
# p2 = Pen("毛笔","狼毫","褐色",50)
# b1 = p1.pen_buy(5)
# b2 = p2.pen_buy(10)
# s1 = Pen.pen_sum(b1,b2)
# print(s1)




"""
采用面向对象编程思想,完成教务管理系统的开发,教务管理系统可以可以管理在校学生的成绩信息,通关控制台菜单与用户交互,具体功能如下:
    1.添加学生成绩,根据输入学生姓名,语文成绩,数学成绩,英语成绩,记录在系统中
        1.1输入学生姓名,语文成绩,数学成绩,英语成绩
        1.2检查学生姓名是否存在,如果不存在,在添加
        1.3验证成绩范围0-100分
        1.4创建学生对象并添加到系统
    2.修改学生成绩,根据输入的学生姓名,修改对应的学生成绩
        2.1输入要修改的学生姓名
        2.2根据姓名查找该学生,显示该生当前成绩信息
        2.3输入要修改的成绩
        2.4更新学生成绩
    3.删除学生成绩,根据输入的学生姓名,删除对应的学生成绩
    4.查询指定学生成绩,根据输入的学生姓名,查找对应的学生成绩并输出
        4.1格式为: "姓名: 张三 | 语文: 90 | 数学: 90 | 英语: 90 | 总分: 270"
    5.展示系统中所有学生成绩
"""
from re import match


# class Student:
#     def __init__(self,name,chinese,math,english):
#         self.name = name
#         self.chainese = chinese
#         self.math = math
#         self.english = english
#
#     def __str__(self):
#         return f"姓名: {self.name} | 语文: {self.chainese} | 数学: {self.math} | 英语: {self.english} | 总分: {self.chainese + self.math + self.english}"
#
#
#     def updete_grade(self,chainese=None,math=None,english=None):
#         if chainese is not None:
#             self.chainese = chainese
#
#         if math is not None:
#             self.math = math
#
#         if english is not None:
#             self.english = english
#
# if __name__ == '__main__':
#     grade = Student(name="张三",chinese=98,math=95,english=83)
#     print(grade)
#     grade.updete_grade(english=93)
#     print(grade)




class StudentSystem:
    def __init__(self):
        self.student_dict = {"张三":{"语文":80,"数学":90,"英语":60},"李四":{"语文":85,"数学":95,"英语":80}}
    #添加学生
    def add_student(self):
        while True:
            name = input("请输入学生姓名:")
            if name in self.student_dict:
                print("该学生已经存在,无法进行添加")
            else:
                break
        chinese = int(input("请输入语文成绩:"))
        math = int(input("请输入数学成绩:"))
        english = int(input("请输入英语成绩:"))
        if 0 <= chinese <=100 and 0 <= math <=100 and 0 <= english <=100:
            self.student_dict[name] = ({"语文":chinese,"数学":math,"英语":english})
            print("学生信息添加成功")
            lost = chinese + math + english
            print(f"姓名: {name} | 语文: {chinese} | 数学: {math} | 英语: {english} | 总分: {lost}")
        else:
            print("请输入正确的学生成绩")

    #修改学生成绩
    def update_student(self):
        name = input("请输入要修改成绩的学生名字:")
        subject = input("请输入要修改成绩的科目:")
        fraction = int(input(f"请输入{subject}新的成绩:"))
        self.student_dict[name][subject] = fraction
        print(f"修改成功,已经将{name}同学的{subject}成绩修改为{fraction}")


    #查询单个学生成绩
    def select_student(self):
        name = input("请输入要查询成绩的学生名字:")
        lost = self.student_dict[name]['语文'] + self.student_dict[name]['数学'] + self.student_dict[name]['英语']
        print(f"姓名: {name} | 语文: {self.student_dict[name]['语文']} | 数学: {self.student_dict[name]['数学']} | 英语: {self.student_dict[name]['英语']} | 总分: {lost}")


    #查询所有学生成绩
    def select_students(self):
        print("正在为你查询所有学生成绩...")
        for i in self.student_dict:
            lost = self.student_dict[i]['语文'] + self.student_dict[i]['数学'] + self.student_dict[i]['英语']
            print(f"姓名: {i} | 语文: {self.student_dict[i]['语文']} | 数学: {self.student_dict[i]['数学']} | 英语: {self.student_dict[i]['英语']} | 总分: {lost}")


    #删除指定学生
    def delete_student(self):
        name = input("请输入要删除的学生姓名")
        self.student_dict.pop(name)
        print(f"已成功删除{name}的成绩!")





    #启动
    def run(self):
        while True:
            print("*"*80)
            print("*"*33,"欢迎使用教务系统","*"*32)
            print("菜单:1.添加学生  2.修改成绩  3.查询单独学生成绩  4.查询所有学生成绩  5.删除学生  6.退出系统")
            print("*"*80)
            try:
                choice = int(input("请选择你的操作:"))
            except ValueError:
                print("请在1-6之间选择操作!")
                continue
            match choice:
                case 1:
                    self.add_student()
                case 2:
                    self.update_student()
                case 3:
                    self.select_student()
                case 4:
                    self.select_students()
                case 5:
                    self.delete_student()
                case 6:
                    break
                case _:
                    print("请在1-6之间选择操作!")

if __name__ == '__main__':
    system = StudentSystem()
    system.run()











