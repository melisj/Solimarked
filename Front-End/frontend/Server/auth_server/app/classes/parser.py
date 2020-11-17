import argparse
import logging as log

class Parser:

    """ 
        Class handles flags and args given at the commandline.

        ...

        Attribute
        ---------
        parser -> Object(argparse)
            Parses the arguments given at the commandline

        args -> Object(result of argparse)
        This where the values are stored from the parser
        
        Methods
        -------
        set_log_levels:
            returns : None
    """

    def __init__(self):
        parser = argparse.ArgumentParser(allow_abbrev=True, description='Parameters\
            for config path and Docker networking')

        # describes the amount of output
        parser.add_argument('-d', '--debug',
            default=False, help="Outputs debug logs",
            action="store_true" )

        parser.add_argument('-i', '--info',
            default=False, help="Outputs info logs",
            action="store_true" )

        parser.add_argument('-w', '--warning',
            default=True, help="Outputs warninglogs",
            action="store_true" )

        parser.add_argument('-e', '--error',
            default=True, help="Outputs error log",
            action="store_true" ) 

        parser.add_argument('-c', '--critical',
            default=True, help="Outputs Critical log",
            action="store_true" )
        
        self.args = parser.parse_args()


    def set_log_levels(self):
        """ 
            Sets the log level; how much is output to stdout
            ....

            Returns:
                None
        """
        if self.args.debug:
            log.basicConfig(level=log.DEBUG)

        elif self.args.info:
            log.basicConfig(level=log.INFO)

        elif self.args.warning:
            log.basicConfig(level=log.WARNING)

        elif self.args.error:
            log.basicConfig(level=log.ERROR)

        elif self.args.critical:
            log.basicConfig(level=log.CRITICAL)
