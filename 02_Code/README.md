# FSEDevBoard package
 
## Installing
      % sudo apt install python3 python3-pip
      % pip3 install virtualenv
      % virtualenv venv -p python3
      % source venv/bin/activate

## Usage
### Instance initialization
      (venv) % cd FSEDevBoard
      (venv) % python3 setup.py sdist
      (venv) % cd dist
      (venv) % pip3 install FseDevBoard-0.0.1.tar.gz

### Running the PDC example
     (venv) % cd ../../applications
     (venv) % python3 PDC.py
