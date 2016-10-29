## HashType base class.
#
# All hash type plugins shall derive from this class. Class-based plugins enable
# multiple instantiations of a particular type of hash format information with
# potentially different requirements
#
class HashType(object):

    ## Initializes the basic HashType plugin values.
    #
    # Derived classes should call this method, like so:
    # \code
    # class RandomHashType(HashType):
    #     def __init__(self):
    #         super().__init__()
    #         # ... plugin specific stuff ...
    # \endcode
    #
    def __init__(self):
        
        self.reference_id="DEFAULT"
        self.display_name="Default"
        additional_fields = []