import subprocess

while True:
    lt = subprocess.Popen(['lt','--port 8000', '--subdomain hbdprincipe'], stdout=subprocess.PIPE)
    output = lt.communicate()[0]
    print output

