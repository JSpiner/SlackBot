from core import add
import random

result = add.delay(random.randint(0,100), random.randint(0,100))
print (result.get())