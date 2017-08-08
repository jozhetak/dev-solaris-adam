"""
    This script is responsible for running multiple Devices in single
    Device Server.
"""

from adam_6217 import ADAM6217
from adam_6224 import ADAM6224
from adam_6250 import ADAM6250

from tango.server import run

def main(args=None, **kwargs):
    return run({'ADAM6217': ADAM6217, 'ADAM6224': ADAM6224,
                'ADAM6250': ADAM6250 },
               args=args, **kwargs)

if __name__ =='__main__':
    main()
