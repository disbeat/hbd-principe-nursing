import subprocess

while True:
    lt = subprocess.call('lt --port 8000 --subdomain hbdprincipe', shell=True)
    print 'error', lt

