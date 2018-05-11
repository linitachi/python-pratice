names = ['Justin', 'caterpillar', 'openhome']

print('for in range')
for i in range(len(names)):
    print(i, '', names[i])
print('for in zip')
i = [0, 1, 2]
for i, element in zip(i, names):
    print(i, '', names[i])
print('for in enumerate')
for i, element in enumerate(names):
    print(i, '', names[i])
