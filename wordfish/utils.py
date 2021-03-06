'''
utils.py
part of the wordfish python tools

Copyright (c) 2015-2018 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to 
do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

from glob import glob
import errno
import tarfile
import zipfile
import requests
import json
import shutil
import os
import re
import pickle


def download_nltk():
    '''download_nltk
       download nltk to home. If it already exists, just return the directory
    '''
    home = os.environ["HOME"]
    download_dir = os.path.abspath(home, 'nltk_data')
    if not os.path.exists(download_dir):
        print("Downloading nltk to %s" %(download_dir))
        import nltk
        nltk.download('all')
    return "%s/nltk_data" %(home)


def save_pretty_json(dict_obj,output_file):
    with open(output_file, 'w') as outfile:
        json.dump(dict_obj,outfile)

def get_installdir():
    return os.path.dirname(os.path.abspath(__file__))

def save_pkl(save_obj,pickle_file):
    pickle.dump(save_obj,open(pickle_file,"wb"))

def mkdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return os.path.abspath(dirname)

def find_subdirectories(basepath):
    '''find_subdirectories
    Return directories (and sub) starting from a base
    '''
    directories = []
    for root, dirnames, filenames in os.walk(basepath):
        new_directories = [d for d in dirnames if d not in directories]
        directories = directories + new_directories
    return directories
    
'''
Make a directory if it doesn't exist

'''

def make_directory(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname

'''
Return directories at one level specified by user
(not recursive)

'''
def find_directories(root,fullpath=True):
    directories = []
    for item in os.listdir(root):
        # Don't include hidden directories
        if not re.match("^[.]",item):
            if os.path.isdir(os.path.join(root, item)):
                if fullpath:
                    directories.append(os.path.abspath(os.path.join(root, item)))
                else:
                    directories.append(item)
    return directories

"""
remove unicode keys and values from dict, encoding in utf8

"""
def remove_unicode_dict(input_dict,encoding="utf-8"):
    output_dict = dict()
    for key,value in input_dict.items():
        if isinstance(input_dict[key],list):
            output_new = [x.encode(encoding) for x in input_dict[key]]
        elif isinstance(input_dict[key],int):
            output_new = input_dict[key]
        elif isinstance(input_dict[key],float):
            output_new = input_dict[key]
        elif isinstance(input_dict[key],dict):
            output_new = remove_unicode_dict(input_dict[key])
        else:
            output_new = input_dict[key].encode(encoding)
        output_dict[key.encode(encoding)] = output_new
    return output_dict

"""
Copy an entire directory recursively

"""
 
def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

"""
get_template: read in and return a template file

"""
def get_template(template_file):
    filey = open(template_file,"rb")
    template = "".join(filey.readlines())
    filey.close()
    return template

def get_attribute(entry, name, default=[]):
    '''A helper to get an attribute from an object, if it exists.
       If not, return some default.'''
    try:
        if hasattr(entry, name):
            return getattr(entry, name)    
    except KeyError:
        pass
    return default

"""
make a substitution for a template_tag in a template
"""
def sub_template(template,template_tag,substitution):
    template = template.replace(template_tag,substitution)
    return template

def save_template(output_file, html_snippet, mode="w"):
    with open(output_file, mode) as filley:
        filey.writelines(html_snippet)
    return output_file

def untar(tar_file,destination="."):
    tar = tarfile.open(tar_file)
    tar.extractall(path=destination)
    tar.close()
    return tar

"""
Check type
"""
def is_type(var,types=[int,float,list]):
    for x in range(len(types)):
        if isinstance(var,types[x]):
            return True
    return False

"""
Ensure utf-8
"""
def clean_fields(mydict):
    newdict = dict()
    for field,value in mydict.items():
        cleanfield = field.encode("utf-8")
        if isinstance(value,float):
            newdict[cleanfield] = value
        if isinstance(value,int):
            newdict[cleanfield] = value
        if isinstance(value,list):
            newlist = []
            for x in value:
                if not is_type(x):
                    newlist.append(x.encode("utf-8"))
                else:
                    newlist.append(x)
            newdict[cleanfield] = newlist
        else:
            newdict[cleanfield] = value.encode("utf-8")
    return newdict

# JOBS #####################################################

def add_lines(script,lines_to_add):
    if isinstance(lines_to_add,str):
        lines_to_add = [lines_to_add]
    lines = []
    if os.path.exists(script):
        filey = open(script,"rb")
        lines = [x.strip("\n") for x in filey.readlines()]
        filey.close()
    for new_line in lines_to_add:
        lines.append(new_line)
    filey = open(script,"wb")
    filey.writelines("\n".join(lines))
    filey.close()

# INTERNET #####################################################################

def get_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def get_json(url):
    '''Return general json'''
    print(url)
    json_single = get_url(url)
    return json.loads(json_single.decode("utf-8"))



def read_file(filename, mode="r"):
    with open(filename,mode) as filey:
        content = filey.read()
    return content


def write_file(filename, content, mode="w"):
    with open(filename, mode) as filey:
        if isinstance(content, list):
            for item in content:
                filey.writelines(content)
        else:
            filey.writelines(content)
    return filename


def read_json(json_file, mode='r'):
    with open(json_file, mode) as filey:
        content = json.load(filey)
    return content

def has_internet_connectivity():
    """has_internet_connectivity
    Checks for internet connectivity by way of trying to
    retrieve google IP address. Returns True/False
    """
    try:
        response = requests.get('http://www.google.com')
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def make_zip(path,out_zip):
    zipper = zipfile.ZipFile(out_zip, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            zipper.write(os.path.join(root, file))
    zipper.close()
    return out_zip
