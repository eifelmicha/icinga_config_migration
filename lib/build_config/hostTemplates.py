from lib.general import *
from notifications import render_notifications

def render(object_hash,contact_hash):
    """
    Function to build the hosttemplates:
    Note that there are states and types now are defined in the Notification template.
    template Host "generic-host" {
      max_check_attempts = 5
      check_interval = 1m
      retry_interval = 30s

      check_command = "hostalive"
    }
    """
    # Default
    default_check_command = 'hostalive'
    write_blocks = 0

    # Header
    header = '# File generated by script, do not edit!\n'
    write_configfile(header)

    # Loop over the templates
    for template in object_hash:

        # Start the configblock
        template_hash = object_hash[template]
        config_block = 'template Host "' + template_hash['name'] + '" {\n'

        debug('--------------------')
        debug(template_hash)

        # Get the needed values
        if 'max_check_attempts' in template_hash:
            config_block += '  max_check_attempts = ' + template_hash['max_check_attempts'] + '\n'
        if 'check_interval' in template_hash:
            config_block += '  check_interval = ' + template_hash['check_interval'] + 'm\n'
        if 'retry_interval' in template_hash:
            config_block += '  retry_interval = ' + template_hash['retry_interval'] + 's\n\n'
        # There has to be a check command defined, if not, use the default
        # @TODO: Move default_check_command to settings
        if 'check_command' in template_hash:
            config_block += '  check_command = "' + template_hash['check_command'] + '"\n'
        else:
            config_block += '  check_command = "' + default_check_command + '"\n'

        # Notifications
        config_block += '\n'
        config_block += render_notifications(template_hash, contact_hash)

        # Close the host configuration block
        config_block += '}\n\n'

        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' hostTemplate objects')
