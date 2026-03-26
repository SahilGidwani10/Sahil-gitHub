class Human:
    def __init__(self,name,age):
        self.name = name 
        self.age = age 
    def show(self):
        print (f"Name: {self.name}")
        print (f"Age: {self.age}")

class Person(Human):
    def __init__(self,name,age,address):
        Human.__init__(self,name,age)
        self.address = address
    def show(self):
        Human.show(self)
        print(f"Address: {self.address}")
        
class Programmer:
    def __init__(self,lang,salary):
        self.lang = lang
        self.salary = salary
    def show(self):
        print (f"Language: {self.lang}")
        print (f"Salary: {self.salary}")
        
class Employee(Person):
    def __init__(self,name,age,address,Programmer):
        Person.__init__(self,name,age,address)
        self.Programmer = Programmer
    def show(self):
        Person.show(self)
        self.Programmer.show()

p = Programmer("Python",100000)
e = Employee("Sahil",25,"kolhapur",p)
e.show()