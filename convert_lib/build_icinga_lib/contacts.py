#!/usr/bin/python2.7
from convert_lib.build_hash import build_hash
from convert_lib.general import debug,info,error,write_configfile,append_configfile
def build_icinga_contacts(object_hash,outputfile,inputdir):
    """Function to build the users:
object User "testconfig-user" {
  import "generic-user"
  display_name = "Icinga Test User"
  email = "icinga@localhost"
}

object UserGroup "icingaadmins" {
  display_name = "Icinga 2 Admin Group"
}   """
    # Default
    groups = build_hash('contactgroup',inputdir)

    # Header
    header = '# File generated by script, do not edit!\n'
    write_configfile(header, outputfile)

    # Loop over the templates
    for contact in object_hash:
        debug('--------------------')
        debug(contact)
        debug(object_hash[contact])

        # Build the config block
        config_block = 'object User "' + contact + '" {\n'
        config_block += '  import "generic-user"\n'
        config_block += '  display_name = "' + object_hash[contact]['alias'] + '"\n'
        config_block += '  email = "' + object_hash[contact]['email'] + '"\n'

        # Get the groups of the user
        contact_group = []
        for group in groups:
            if contact in groups[group]['members']:
                contact_group.append(group)
                debug('Found contact in: ' + group)
        if not contact_group == []:
            config_block += '  groups = [ "' + '", "'.join(contact_group) + '" ]\n'
        else:
            pass

        # Close config block
        config_block += '}\n'

        debug('\n' + config_block)
        append_configfile(config_block,outputfile)

    append_configfile('# Groups\n',outputfile)

    # Also build the contactgroups
    for group in groups:
        config_block = 'object UserGroup "' + group + '" {\n'
        config_block += '  display_name = "' + groups[group]['alias'] + '"\n'
        config_block += '}\n'
        debug('\n' + config_block)
        append_configfile(config_block,outputfile)

