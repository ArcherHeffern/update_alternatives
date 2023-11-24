ULS = ''  # Underline start
ULE = ''  # Underline end
ITS = ''  # Italic start
ITE = ''  # Italic end

description = f'''
Uncomplicated port of the Debian alternatives system. Please refer to Update-Alternatives(1) for an introduction into the basic concepts and functionality this tool manages
'''

general = f'''Uncomplicated port of the Debian alternatives system. 

        It is possible for several programs fulfilling the same or
        similar functions to be installed on a single system at the same
        time.  For example, many systems have several text editors
        installed at once.  This gives choice to the users of a system,
        allowing each to use a different editor, if desired, but makes it
        difficult for a program to make a good choice for an editor to
        invoke if the user has not specified a particular preference.

        Debian's alternatives system aims to solve this problem.  A
        generic name in the filesystem is shared by all files providing
        interchangeable functionality.  The alternatives system and the
        system administrator together determine which actual file is
        referenced by this generic name.  For example, if the text
        editors ed(1) and nvi(1) are both installed on the system, the
        alternatives system will cause the generic name /usr/bin/editor
        to refer to /usr/bin/nvi by default. The system administrator can
        override this and cause it to refer to /usr/bin/ed instead, and
        the alternatives system will not alter this setting until
        explicitly requested to do so.

        Terminology: 
        Since the activities of update-alternatives are quite involved, some specific terms will help to explain its operation.

        Generic name (alternative link)
        A name, like /usr/bin/editor, which refers, via the alternatives system, to one of a number of files of similar function.

        alternative name
        The name of a symbolic link in the alternatives directory.

        alternative (or alternative path)
        The name of a specific file in the filesystem, which may be made accessible via a generic name using the alternatives system.

        alternatives directory
        A directory, by default /usr/local/etc/alternatives, containing the symlinks.

        administrative directory
        A directory, by default /usr/local/var/lib/dpkg/alternatives, containing update-alternatives' state information.

        link group
        A set of related symlinks, intended to be updated as a group.

        '''

new = f'Create a new link'

add = f'Add an alternative to an exisiting link group'

set_ = f'Set an alternative as main alternative of a link group'

remove = f'Remove an alternative from a link group'

remove_all = f'Remove a link group'

display = f'Display information about a link group'

display_all = f'Display information about all link groups'
