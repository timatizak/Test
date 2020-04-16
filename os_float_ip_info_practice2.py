from __future__ import absolute_import, division, print_function
__metaclass__ = type
import json

ANSIBLE_METADATA = {'status': ['preview'],
          'supported_by': 'community',
          'version': '1.1'}

def _get_floating_ip(cloud, floating_ip_address):
    f_ips = cloud.search_floating_ips(
        filters={'floating_ip_address': floating_ip_address})
    if not f_ips:
        return None

    return f_ips[0]

def _get_serverid_timur(cloud, identity):
    id_s = cloud.search_servers(
        filters={'identity' : id})
    if not id:
        return None

    return id_s[0]

def main():
  argument_spec = openstack_full_argument_spec(
    name=dict(required=False),
    public_key=dict(required=False),
    filters=dict(type='dict', required=False),
    all_projects=dict(required=False, type='bool', default=False),
    detailed=dict(required=False, type='bool', default=False),
    server=dict(required=False),
    floating_ip_address=dict(required=False, default=None), 
  )

  module_kwargs = openstack_module_kwargs()

  module = AnsibleModule(argument_spec,**module_kwargs)

  server_name_or_id = module.params['server'] 
  floating_ip_address = module.params['floating_ip_address']
  name = module.params['name']
  public_key = module.params['public_key']
  filters = module.params['filters']
  all_projects=module.params['all_projects']
  server_name_or_id = module.params['server']
  sdk, cloud = openstack_cloud_from_module(module)
  try:
    servers = cloud.search_servers(detailed=module.params['detailed'], filters=module.params['filters'], all_projects=module.params['all_projects'])
    for server in servers:
      public_ip = cloud.get_server_public_ip(server)
      internal_ip = cloud.get_floating_ip(public_ip) 

    module.exit_json(server=server, ip=ip, internal_ip=internal_ip)
  except sdk.OpenStackCloudException as e:
    module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
if __name__ == '__main__':
  main()
