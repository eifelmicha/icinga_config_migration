#!/usr/bin/python2.7
from convert_lib.general import debug,info,error,write_configfile,append_configfile
def build_icinga_hostTemplates(object_hash,outputfile):
    """Function to build the hosttemplates:
    Note that there are states and types now are defined in the Notification template.
template Host "generic-host" {
  max_check_attempts = 5
  check_interval = 1m
  retry_interval = 30s

  check_command = "hostalive"
}   """
    # Default
    default_check_command = 'hostalive'

    # Header
    header = '# File generated by script, do not edit!\n'
    write_configfile(header, outputfile)

    # Loop over the templates
    for template in object_hash:
        # Start the configblock
        template_hash = object_hash[template]
        debug('--------------------')
        debug(template_hash)
        config_block = 'template Host "' + template_hash['name'] + '" {\n'
        if 'max_check_attempts' in template_hash:
            config_block += '  max_check_attempts = ' + template_hash['max_check_attempts'] + '\n'
        if 'check_interval' in template_hash:
            config_block += '  check_interval = ' + template_hash['check_interval'] + 'm\n'
        if 'retry_interval' in template_hash:
            config_block += '  retry_interval = ' + template_hash['retry_interval'] + 's\n\n'
        if 'check_command' in template_hash:
            config_block += '  check_command = "' + template_hash['check_command'] + '"\n'
        else:
            config_block += '  check_command = "' + default_check_command + '"\n'
        config_block += '}\n\n'

        append_configfile(config_block,outputfile)
