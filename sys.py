student = [] 
def studentMeau(): 
 print('-'*30) 
 print('-------学生信息管理系统-------') 
 print('  1、添加学生信息') 
 print('  2、删除学生信息') 
 print('  3、查询学生信息')  
 print('  4、修改学生信息') 
 print('  5、退出') 
 print('-'*30) 
def appendStuInf(): 
 studentInf = {'Name':'','Id':'','Sex':'','Age':'','Project':''} 
 studentInf['Name'] = input('请输入学生姓名：') 
 studentInf['Id'] = input('请输入学生学号：') 
 studentInf['Sex'] = input('请输入学生性别：') 
 studentInf['Age'] = input('请输入学生年龄：') 
 studentInf['Project'] = input('请输入学生专业：') 
 student.append(studentInf) 
 #print(student) 
def deleteStuInf(): 
 num = input('请输入要删除学生的学号：') 
# for i in range(len(student)): 
#  if student[i]['Id'] == num: 
#   student.remove(student[i]) 
#   break 
 for stu_inf in student: 
  if stu_inf['Id'] == num: 
   student.remove(stu_inf) 
   break
# print(student) 
def inquireStuInf(): 
 flag = False
 num = input('请输入要查询学生的学号：') 
 for stu_inf in student: 
  if stu_inf['Id'] == num: 
   print('name: '+stu_inf['Name']+'\n') 
   print('Id: '+stu_inf['Id']+'\n') 
   print('Sex: '+stu_inf['Sex']+'\n') 
   print('Age: '+stu_inf['Age']+'\n') 
   print('Project: '+stu_inf['Project']+'\n') 
   flag = True
   break
 if flag == False: 
  print('没有查询到该生的信息！') 
def modifyStuInf(): 
 num = input('请输入要修改学生的学号：') 
 flag = False
 for stu_inf in student: 
  if stu_inf['Id'] == num: 
   print('name: '+stu_inf['Name']+'\n') 
   print('Id: '+stu_inf['Id']+'\n') 
   print('Sex: '+stu_inf['Sex']+'\n') 
   print('Age: '+stu_inf['Age']+'\n') 
   print('Project: '+stu_inf['Project']+'\n') 
   flag = True
   break
 if flag == False: 
  print('没有该生的信息！') 
  return
 print('1:姓名 ---- 2:学号 ---- 3:性别 ---- 4:年龄 ---- 5:专业 ---- 6:退出'+'\n') 
 while True: 
  choice = int(input("请输入选项序号：")) 
  if choice == 1: 
   stu_inf['Name'] = input('请重新输入姓名：') 
   print('姓名已更正为：'+stu_inf['Name']+'\n') 
  elif choice == 2: 
   stu_inf['Id'] = input('请重新输入学号：') 
   print('学号已更正为：'+stu_inf['Id']+'\n') 
     
  elif choice == 3: 
   stu_inf['Sex'] = input('请重新输入性别：') 
   print('性别已更正为：'+stu_inf['Sex']+'\n') 
  elif choice == 4: 
   stu_inf['Age'] = input('请重新输入年龄：') 
   print('年龄已更正为：'+stu_inf['Age']+'\n') 
  elif choice == 5: 
   stu_inf['Project'] = input('请重新输入专业：') 
   print('专业已更正为：'+stu_inf['Project']+'\n') 
  elif choice == 6: 
   print('修改完毕！') 
   break
  else: 
   print('输入有误，不予执行!') 
while True: 
 studentMeau() 
 choice = int(input("请输入选项序号：")) 
 if choice == 1: 
  #添加学生信息 
  appendStuInf() 
 elif choice == 2: 
  #删除学生信息 
  deleteStuInf() 
 elif choice == 3: 
  #查询学生信息 
  inquireStuInf() 
 elif choice == 4: 
  #修改学生信息 
  modifyStuInf() 
 elif choice == 5: 
  print('谢谢使用！') 
  break
 else: 
  print('输入有误，检查后重新输入！') 
