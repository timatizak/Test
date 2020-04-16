from __future__ import absolute_import, division, print_function
__metaclass__ = type
import json

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

def _get_floating_ip(cloud, floating_ip_address, fixed_ip_address):
    f_ips = cloud.search_floating_ips()
    if not f_ips:
        return None

    return f_ips[0]


def main():

    argument_spec = openstack_full_argument_spec(
        server=dict(required=False),
        port=dict(required=False),
        filters=dict(type='dict', required=False),
        floating_ip_address=dict(required=False, default=None),
        all_projects=dict(required=False, type='bool', default=False),
        detailed=dict(required=False, type='bool', default=False),
    )


    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    server_name_or_id = module.params['server']
    floating_ip_address = module.params['floating_ip_address']
    port = module.params['port']
    filters = module.params['filters']
    all_projects=module.params['all_projects']
    sdk, cloud = openstack_cloud_from_module(module)
    try:

       openstack_servers = cloud.search_servers(detailed=module.params['detailed'], filters=module.params['filters'], all_projects=module.params['all_projects'])
       f_ips = cloud.search_floating_ips()

       #ports = cloud.search_ports(port, filters)
       #server = cloud.get_server(server_name_or_id)
       #fip_address = cloud.get_server_public_ip(server)
       #module.exit_json(changed=False, openstack_servers=openstack_servers, openstack_ports=ports)
       #module.exit_json(changed=False, openstack_ports=ports)
       """for server in openstack_servers:
           fip_address = cloud.get_server_public_ip(server)
           ip  = cloud.get_floating_ip(fip_address)
           print(json.dumps({
                     "floating_ip": ip,
                     "public_ip" : fip_address
           }))"""
       floating_ip_address = cloud.get_floating_ip(id)
       module.exit_json(f_ips=floating_ip_address)
       #module.exit_json(floating_ip=ip, public_ip=fip_address)
       #floating_ip = cloud.get_interface_ip(openstack_servers)
       #module.exit_json(changed=False)
       #module.exit_json(changed=False, ip=f_ips)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e, ip, fip_address))

from ansible.module_utils.basic import AnsibleModule, remove_values 
from ansible.module_utils.openstack import (openstack_full_argument_spec, openstack_module_kwargs, openstack_cloud_from_module)
if __name__ == '__main__':
    main()
