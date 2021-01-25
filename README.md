# Acl2_bridge - Connect to an ACL2 Server from Python

With Acl2_bridge, you can connect to an [ACL2](https://www.cs.utexas.edu/users/moore/acl2/) server running the 
[ACL2::Bridge](https://www.cs.utexas.edu/users/moore/acl2/manuals/current/manual/index.html?topic=ACL2____BRIDGE). 
Note that you must have an ACLw2 server running for this package to be useful.

## Usage

To download this package, simply fork this github repo or use Pypy via pip;

    $ pip install acl2_bridge

To use it, import the acl2_bridge package, connect to an ACL2 server, and issue ACL2 commands:

    from acl2_bridge import ACL2Command, ACL2Bridge
    
    bridge = ACL2Bridge()
    response = bridge.acl2_command(ACL2Command.JSON, "(cdr (assoc 'acl2-version *initial-global-table*))")
    print ("Connected to:", response["RETURN"])

## LICENSE

This package is released with the same license as ACL2, the BSD 3-Clause license.
