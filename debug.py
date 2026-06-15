import os

print('CWD:', os.getcwd())
print('Templates exists:', os.path.exists('templates'))
print(os.listdir('templates') if os.path.exists('templates') else 'NO TEMPLATES')

