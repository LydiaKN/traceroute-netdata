from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    status_set,
)
from charms.reactive import (
    clear_flag,
    set_flag,
    when,
    when_not,
)
import charms.sshproxy


@when('sshproxy.configured')
@when_not('charm3.installed')
def install_charm3():
    set_flag('charm3.installed')
    status_set('active', 'Ready!')

@when('actions.remove')
def remove():
    cmd = []
    err = ''
    try:
        address = action_get('address')
        address=address.replace('.','_')
        cmd = ['sudo rm /usr/libexec/netdata/python.d/dest{}.chart.py; sudo systemctl restart netdata'.format(address)]
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'output': result})
    finally:
        clear_flag('actions.remove')

