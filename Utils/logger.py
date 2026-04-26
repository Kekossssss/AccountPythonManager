VERBOSE = 0

def set_verbose_level(verbose:int):
    global VERBOSE
    VERBOSE = verbose

def print_info(msg):
    if (VERBOSE > 0):
        print(f"INFO : {msg}")

def print_basic(msg):
    if (VERBOSE > 1):
        print(f"DEBUG (BASIC) : {msg}")

def print_advanced(msg):
    if (VERBOSE > 2):
        print(f"DEBUG (ADVANCED) : {msg}")

def print_detail(msg):
    if (VERBOSE > 3):
        print(f"DEBUG (DETAILLED) : {msg}")