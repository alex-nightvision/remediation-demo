# Remediation Demo

A flask app with SQL injection to be used for remediation demo.


- http://127.0.0.1:5000/users?name=%27%20OR%20%271%27=%271
- http://127.0.0.1:5000/users?name='%20OR%20'1'='1

```
curl "http://127.0.0.1:5000/users?name='%20OR%20'1'='1"
```