# FylUpload

#### Deploying Flask to IIS and installing Python
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

#### Data Model
1. Create/edit all tables through IDE, not directly in database
2. Any table that you want to upload a file to, add the field `FileUploadID NVARCHAR(50)` to the data model

#### HTML Template
1. Create new Template via Look & Feel in the IDE
2. Copy the code from `template.html` into the Template content, replacing `src=""` with the URL of the Flask application created above
3. Create new Page Control of type HTML and select the newly created Template

#### Uploading a File
1. Enter the target Database & Table Names
2. Browse and select a *.csv* file 
3. Checking `Truncate target table?` will truncate the selected table before inserting new records from the file
4. By default, the upload will insert into the column names of the CSV file. If there are extra columns, or column names that do not exactly match the table column (case sensitive), the upload will error out.
  - Checking `Ignore non-matching fields?` will insert *only* into columns where the name from the CSV exactly matches the name in the target table.
5. On error, an error messsage will be displayed below.  On success, the page will refresh.



