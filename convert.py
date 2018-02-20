#!/usr/bin/python2.7
"""
Main entry point for generating the icinga2 compatible config.

Need to add examples and more information on how to use this utility.
"""
import sys
import getopt
import os
# Custom libs
from convert_lib.general import debug,info,error,write_configfile,append_configfile
from convert_lib.build_hash import build_hash
from convert_lib.build_icinga_lib.hosts import build_icinga_hosts
from convert_lib.build_icinga_lib.commands import build_icinga_commands
from convert_lib.build_icinga_lib.services import build_icinga_services
from convert_lib.build_icinga_lib.hostTemplates import build_icinga_hostTemplates
from convert_lib.build_icinga_lib.contacts import build_icinga_contacts
from convert_lib.build_icinga_lib.serviceTemplates import build_icinga_serviceTemplates

# Locations of the input dirs ( hardcoded for now )
inputdir='/home/bjanssens/Documents/centreon/original/centreon-engine/'
outputdir='/home/bjanssens/Documents/centreon/converted/'
#inputdir='/mnt/home/bjanssens/Documents/centreon/original/centreon-engine/'
#outputdir='/mnt/home/bjanssens/Documents/centreon/converted/'

# Default params
# Figure out how global parameters work in python
debug_setting = False

def build_icinga_config(write, object_name):
    """Function to build the icinga config"""
    # Create if does not exists
    outputfile = outputdir + object_name + '.conf'

    # Use the fancy build_hash
    object_hash = build_hash(object_name,inputdir)

    # Depending on the object type different actions need to be taken
    if object_name in ['host']:
        build_icinga_hosts(object_hash,outputfile,inputdir)
    elif object_name in ['hostTemplate']:
        build_icinga_hostTemplates(object_hash,outputfile)
    elif object_name in ['serviceTemplate']:
        build_icinga_serviceTemplates(object_hash,outputfile,inputdir)
    elif object_name in ['service']:
        build_icinga_services(object_hash,outputfile,inputdir)
    elif object_name in ['command']:
        build_icinga_commands(object_hash,outputfile)
    elif object_name in ['contact']:
        build_icinga_contacts(object_hash,outputfile,inputdir)
    elif object_name in ['notification']:
        debug('Not ready yet')

def main():
    # Default
    global debug_setting
    global inputdir
    global outputdir
    write = False
    # Getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "wdo:I:O:", ['write','debug', 'object=', 'input=','output='])
    except getopt.GetoptError as err:
        error( str(err))
    for o,a in opts:
        if o in ("-d", "--debug"):
            debug_setting = True
            debug('Debugging is ON')
        elif o in ( "-w", "--write"):
            write = True
        elif o in ( "-o", "--object"):
            object_name = a
        elif o in ( "-I", "--input"):
            inputdir = a
        elif o in ( "-O", "--output"):
            outputdir = a
        else:
            assert False

    if not object_name in ['host','service','serviceTemplate','notification','contact','hostgroup','servicegroup','contactgroup','hostTemplate','command']:
        error("Object not known")
    if not os.path.isdir(inputdir):
        error("Input directory does not exist!")
    if not os.path.isdir(outputdir):
        error("Output directory does not exist!")
    if not inputdir.split('/').pop(-1) == '':
        # Add tailing / to the inputdir
        inputdir = inputdir + '/'
    if not outputdir.split('/').pop(-1) == '':
        # Add tailing / to the outputdir
        outputdir = outputdir + '/'

    build_icinga_config(write, object_name)

if __name__ == "__main__":
    main()
