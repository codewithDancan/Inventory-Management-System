class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def student_data(self):
        print("Your name is ", self.name)
        print("Your age is ", self.age)

    def setlanguage(self, language):
        self.language = language

    def getlanguage(self):
        return self.language

demo = Student("Dancan", 20)
demo.setlanguage("Python")
print(demo.getlanguage())
print(demo.age)

demo.student_data()
