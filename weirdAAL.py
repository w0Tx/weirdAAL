# This file will help to serve as a starting point for using the rest of the tools
# Things we want to figure out
# 1) Is your key active?
# 2) If active, can you read monitoring configs, can you write?
# 3) Okay, you can read monitoring configs. We recommend things to avoid. Want to go further? Use write access to disable (if applicable)
# 4) Don't want to do anything with monitoring? That's fine, let's guide you through figuring out what your access looks like
# 5) Help with a printout of options from this point forward

import boto3
import argparse
import os
import botocore
#from botocore.exceptions import ClientError
#from botocore.exceptions import ConfigParseError
from modules import *
import sys
import builtins
import re
from collections.abc import Iterable
from collections import namedtuple
import textwrap

# Let a user set .aws/credentials or another file as the credentials source
# If user-defined, must be an absolute path
#if 'AWS_SHARED_CREDENTIALS_FILE' not in os.environ:
#    try:
#        #  print("loading .env into our ENV")
#        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '.env'
#    except Exception as e:
#        print("Error: {}".format(e))
#        sys.exit("fix your credentials file -exiting...")

# If you want to use a transparent + supports SSL proxy you can put it here
# os.environ['HTTPS_PROXY'] = 'https://127.0.0.1:3128'

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--module", help="list the module you would like to run", action="store", type=str, required=False)
parser.add_argument("-t", "--target", help="Give your target a name so we can track results", action="store", type=str, required=False)
parser.add_argument("-a", "--arguments", help="Provide a list of arguments, comma separated. Ex: arg1,arg2,arg3", action="store", type=str, required=False)
parser.add_argument("-l", "--list", help="list modules", required=False, action="store_true")
parser.add_argument("-p", "--profile", help="AWS CLI profile if multiple exists in credentials file", action="store", type=str, required=False)
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
args = parser.parse_args()

# Provides us with a global var "db_name" we can access anywhere
builtins.db_name = "weirdAAL.db"

if args.profile:
    os.environ['AWS_PROFILE'] = args.profile


def perform_credential_check():
    '''
    Check that the AWS keys work before we go any further. It picks the keys up from the local .env file
    We are letting boto3 do all the work that way we can handle session tokens natively
    '''

    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        #client = boto3.client("sts")
        #account_id = client.get_caller_identity()["Account"]
        print(f"[+] Successfully authenticated with {credentials.access_key}")
    except AttributeError:
        print("[X] Didn't find credentials in ~/.aws/credentials")
        sys.exit(1)
    except (botocore.exceptions.NoCredentialsError) as e:
        print("[X] Unable to locate credentials")
        sys.exit("fix your credentials file -exiting...")
    except botocore.exceptions.ClientError as e:
        print("[X] The AWS Access Keys are not valid/active [X]")
        sys.exit(1)

def method_create():
    try:
        arg = globals()["module_" + args.module]
        return arg
    except KeyError:
        print("That module does not exist")
        exit(1)

builtins.aws_module_methods_info = {}
builtins.gcp_module_methods_info = {}

def get_methods_for_classname(classname):
    methods = []
    all_methods = dir(sys.modules[classname])
    for meth in all_methods:
        if meth.startswith("module_"):
            narg = "{}.__doc__".format(meth)
            narg = eval(narg)
            nhash = {}
            nhash[meth] = narg
            methods.append(nhash)
    return methods


def make_list_of_methods(cloud_service, mod):
    meths = get_methods_for_classname(mod)
    if cloud_service == 'aws':
        new_mod_name = re.sub("modules.aws.", "", mod)
        aws_module_methods_info[new_mod_name.upper()] = meths
    elif cloud_service == 'gcp':
        new_mod_name = re.sub("modules.gcp.", "", mod)
        gcp_module_methods_info[new_mod_name.upper()] = meths


def make_the_list():
    for m in sys.modules.keys():
        if (m.startswith("modules.aws")
        and not (m == "modules.aws")):
            make_list_of_methods("aws", m)
        elif ((m.startswith("modules.gcp"))
        and not (m == "modules.gcp")):
            make_list_of_methods("gcp", m)

def normalize_comments(string):
    string = textwrap.fill(string.strip(), 40)
    return string


def make_tabulate_rows(hash, cloud_provider):
    entire_contents = []
    for (key) in hash:
        for item in hash[key]:
            for (k,v) in item.items():
                normalized_comment = normalize_comments(v)
                k = re.sub("module_", "", k)
                entire_contents.append([cloud_provider, key, k, normalized_comment])

    return entire_contents

def print_the_list():
    aws_rows = make_tabulate_rows(aws_module_methods_info, 'AWS')
    gcp_rows = make_tabulate_rows(gcp_module_methods_info, 'GCP')
    print(tabulate(aws_rows, headers=['Cloud Provider', 'Service', 'Mod', 'Desc']))
    print(tabulate(gcp_rows, headers=['Cloud Provider', 'Service', 'Mod', 'Desc']))

if (args.list):
    make_the_list()
    print_the_list()
    sys.exit(1)

# Need to figure out if we have keys in the ENV or not
perform_credential_check()

sys.path.append("modules")
for module in all_modules:
    exec("from %s import *" % module)

# arg_list has to be defined otherwise will cause an exception
arg_list = None

if (args.arguments):
    arg_list = args.arguments.split(',')

# We need the user to tell us the module they want to proceed on
if (args.module):
    if not (args.target):
        print("Use -t to give your target a name so we can track results!!!")
        sys.exit(1)
    else:
        # Provides us with a global var "target" we can access anywhere
        builtins.target = args.target
        arg = method_create()
        if callable(arg):
            if arg_list:
                arg(arg_list)
            else:
                arg()

# Allow the user to specify verbosity for debugging
if (args.verbosity):
    print("Verbosity is enabled")
