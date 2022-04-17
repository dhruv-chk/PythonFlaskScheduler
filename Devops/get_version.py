import json

f = open('version.json', 'r')
version_data = json.load(f)
f.close()

print(version_data['version'])
