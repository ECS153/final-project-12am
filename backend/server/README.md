How to run Flask app?
 
1. Set up virtual environment LOCALLY (one dir above the whole project dir)
    - run `python -m venv venv`

2. Activate your virtual environment    
    - run `source venv/bin/activate`
    - succeeded installed example: `(venv) KennydeMacBook-Pro:backend kennyli$` 
    - deactivaten by `deactivate venv`

3. Install dependencies (first navigate to dir with requirements.txt)
    - run `pip install -r requirement`

4. Run Flask App (first navigate to dir `server`)
    - run `flask run`
    
5. *Mac Port-In-Used error
    - find port id: `ps -fA | grep python` 
    - copy the second number of the first line which is the <PID> you need
    - terminate process: `sudo lsof -i:8080 | kill <PID>`
    
6. *Other dependencies related errors
    - run `pip install <LIB> --upgrade`
    - or run `pip install --upgrade pip`

  