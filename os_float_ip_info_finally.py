ANSIBLE_METADATA = {'status': ['preview'],
          'supported_by': 'community',
          'version': '1.1'}

def main():
  argument_spec = openstack_full_argument_spec(
    name=dict(required=False),
    public_key=dict(required=False),
    filters=dict(type='dict', required=False),
    all_projects=dict(required=False, type='bool', default=False),
    detailed=dict(required=False, type='bool', default=False),
  )

  module_kwargs = openstack_module_kwargs()
  module = AnsibleModule(argument_spec,**module_kwargs)

  name = module.params['name']
  public_key = module.params['public_key']
  filters = module.params['filters']
  all_projects=module.params['all_projects']
  sdk, cloud = openstack_cloud_from_module(module)
  try:
    servers = cloud.search_servers(detailed=module.params['detailed'], filters=module.params['filters'], all_projects=module.params['all_projects'])
    my_task=[{'private_ip':cloud.get_server_private_ip(server),'public_ip':cloud.get_server_public_ip(server), 'server_id':cloud.get_server_id(server)} for server in servers]

    module.exit_json(my_task=my_task)
  except sdk.OpenStackCloudException as e:
    module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *
if __name__ == '__main__':
  main()
