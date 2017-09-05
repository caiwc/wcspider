import sys
from management import execute_command

# execute_command(['manage.py','startcrawl','testspider'])
execute_command(sys.argv)