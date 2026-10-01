# 错误写法：from test_faker import Faker
# 正确写法：导入的是安装的第三方库 faker
from faker import Faker
import random

fake = Faker()

students = [(fake.first_name(), random.randint(50, 100)) for _ in range(5)]
print(students)