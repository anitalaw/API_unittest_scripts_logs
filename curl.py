import os
import pdb


test = """
# get date
curl -i -H "Content-Type: application/json" -X GET -d'{"full":true}' http://localhost:5000/dates
curl -i -H "Content-Type: application/json" -X GET -d'{"full":false}' http://localhost:5000/dates
curl http://localhost:5000/dates
curl -i -H "Content-Type: application/json" -X GET -d'{"full":"exts"}' http://localhost:5000/dates
"""

test_time = """
# get time
curl http://localhost:5000/time
curl -i -H ""Content-Type: application/json" -X GET -d'{"military": false, "full": false}' http://localhost:5000/time
curl -i -H ""Content-Type: application/json" -X GET -d'{"military": true, "full": false}' http://localhost:5000/time
curl -i -H ""Content-Type: application/json" -X GET -d'{"military": false, "full": true}' http://localhost:5000/time
curl -i -H ""Content-Type: application/json" -X GET -d'{"military": true, "full": true}' http://localhost:5000/time
"""

tokenize_test = test.strip().split('\n')

for cmd in tokenize_test:
    if not cmd.startswith('#'):
        print(f'##### NEW TEST ######')
        os.system(cmd)
        print('\n')

tokenize_test_time = test.strip().split('\n')

for cmd in tokenize_test_time:
    if not cmd.startswith('#'):
        print(f'##### NEW TEST ######')
        os.system(cmd)
        print('\n')