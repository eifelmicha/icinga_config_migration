#!/usr/bin/python2.7
from convert_lib.general import debug,info,error,write_configfile,append_configfile
from convert_lib.build_hash import build_hash
from commands import build_icinga_commands
from collections import OrderedDict

def build_icinga_serviceTemplates(object_hash,outputfile,inputdir):
    """Function to build the icinga services templates file:
template Service "generic-service" {
  max_check_attempts = 3
  check_interval = 1m
  retry_interval = 30s
}
    """
    # Header
    header = '# File generated by script, do not edit!\n'
    write_configfile(header, outputfile)

    #Defaults
    write_blocks = 0
    pass_commands = OrderedDict({})
    commands_hash = build_icinga_commands(build_hash('command',inputdir),'dummydir',False)

    for service in object_hash:
        debug('--------------------')
        debug(service)
        debug('--------------------')
        debug(object_hash[service])

        # Define config_block
        config_block= 'template Service "' + object_hash[service]['name'] + '" {\n'

        # Check for common params
        if 'use' in object_hash[service] and 'check_command' in object_hash[service]:
            config_block += '  import "' + object_hash[service]['use'] + '"\n'
        elif 'check_command' in object_hash[service]:
            config_block += '  import "generic-service"\n'
        else:
            pass

        if 'max_check_attempts' in object_hash[service]:
            config_block += '\n'
            config_block += '  max_check_attempts = ' + object_hash[service]['max_check_attempts'] + '\n'
        if 'check_interval' in object_hash[service]:
            config_block += '  check_interval = ' + object_hash[service]['check_interval'] + 'm\n'
        if 'retry_interval' in object_hash[service]:
            config_block += '  retry_interval = ' + object_hash[service]['retry_interval'] + 's\n'


        # Check if there is a check_command defined
        if 'check_command' in object_hash[service]:

            # Spacer
            config_block += '\n'

            # Setup the check_command
            check_command = object_hash[service]['check_command']

            # Check if it's a list
            if isinstance(check_command,list):
                check_command = ','.join(check_command)

            # Check if it passes args
            if '!' in check_command:
                check_command_list = check_command.split('!')

                # Get the check_command
                check_command = check_command_list.pop(0)
                #debug("Check_command: " + check_command)
                config_block += '  check_command = "' + check_command + '"\n'

                # Get the arguments of the command
                arguments = commands_hash[check_command]
                #debug('Arguments: ' + str(arguments))

                # Build the values to pass
                argument_i = 0
                for key in arguments:
                    # Check if the value of the key is $ARG\n$
                    if arguments[key] in ['$ARG1$','$ARG2$','$ARG3$','$ARG4$']:
                        key = 'vars.' + check_command.replace('-','_') + '_' + key.translate(None, '-')
                        value = check_command_list[argument_i]
                        config_block += '  ' + key + ' = "' + value + '"\n'
                        argument_i+= 1
                    else:
                        pass

            # No arguments in for the check_command
            else:
                config_block += '  check_command = "' + object_hash[service]['check_command'] + '"\n'
        # Close the config block
        config_block += '}\n'
        #debug('complete config block:\n' + config_block)

        # Write the config file
        append_configfile(config_block, outputfile)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' serviceTemplate objects')
