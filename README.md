# Remediation Demo

A flask app with SQL injection to be used for remediation demo.


- http://127.0.0.1:5000/users?name=%27%20OR%20%271%27=%271
- http://127.0.0.1:5000/users?name='%20OR%20'1'='1

```
curl "http://127.0.0.1:5000/users?name='%20OR%20'1'='1"
```

## Local Setup

```
nightvision app create -n remediation-demo
nightvision target create -n remediation-demo -u http://127.0.0.1:5000/ --type api
nightvision swagger extract ./ -t remediation-demo --lang python 
pip install -r requirements.txt
python app.py
nightvision scan -t remediation-demo -a remediation-demo
 ```