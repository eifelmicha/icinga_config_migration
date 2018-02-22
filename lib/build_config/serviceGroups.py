from lib.general import *
from lib.build_hash import build_hash

def render(object_hash):
    """
    @TODO: Add a description here
    """

    # Header
    write_configfile(settings.header)

    # Defaults
    write_blocks = 0

    for serviceGroups in object_hash:

        # Init config block
        config_block = ''

        # Write configblock
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' serviceGroups objects')
