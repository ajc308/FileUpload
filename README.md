# FylUpload

1. Follow Setup Instructions for deploying Flask App to IIS: http://netdot.co/2015/03/09/flask-on-iis/ 

2. Install Flask: 
 ```shell
 pip install flask
 ```

3. Install pymssql pre-reqs:  
 - [Add C++ and Python tools to Visual Studio Installation](http://stackoverflow.com/questions/28251314/error-microsoft-visual-c-10-0-is-required-unable-to-find-vcvarsall-bat )
 
4. Set environment variables to use VS 2015 instead of older versions to find Visual C++
 ```shell
 SET VS90COMNTOOLS=%VS140COMNTOOLS%
 SET VS100COMNTOOLS=%VS140COMNTOOLS%
 ```
 
5. Install previous version of pymssql for FreeTDS Support: 
 ```shell
 pip install pymssql==2.1.1
 ```
