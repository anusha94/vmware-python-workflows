'''
The REST APIs provide a limited set of details for the VMs.
To list the VMs using REST bindings, refer https://github.com/vmware/vsphere-automation-sdk-python/blob/master/samples/vsphere/vcenter/vm/list_vms.py

If using pyvmomi, the vm.summary.config object should give you a whole bunch of details
Refer to https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/getallvms.py

This sample will demonstrate how to get vm using,
vm-id (REST)
vm-name (pyvmomi)
instance-uuid (pyvmomi)
bios-uuid (pyvmomi)
'''

from vmware.vapi.vsphere.client import create_vsphere_client
from utils.cli_parser import parser

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim


import requests

requests.packages.urllib3.disable_warnings()


parser.add_argument("--vm_name",
                    help="name of the vm")
parser.add_argument("--vm_id",
                    help="id of the vm")
parser.add_argument("--instance_uuid",
                    help="instance uuid of the vm")
parser.add_argument("--bios_uuid",
                    help="bios uuid of the vm")

args = parser.parse_args()

session = requests.session()
session.verify = False if args.skipverification else None

# REST client
vsphere_client = create_vsphere_client(server=args.server,
                                        username=args.username,
                                        password=args.password,
                                        session=session)


# pyvmomi connection instance
if args.skipverification:
    service_instance = connect.SmartConnectNoSSL(host=args.server,
                                                user=args.username,
                                                pwd=args.password,
                                                port=443)


content = service_instance.content
search_index = content.searchIndex
root_folder = content.rootFolder
container = content.viewManager.CreateContainerView(root_folder, [vim.VirtualMachine], True)   

virtual_machines = {}
for managed_object_ref in container.view:
    virtual_machines.update({managed_object_ref: managed_object_ref.name})



# list all VMs using REST bindings
#vms = vsphere_client.vcenter.VM.list()


# get vm from vm-id using REST bindings
# the get() method accepts only the vm-id
if args.vm_id:
    vm = vsphere_client.vcenter.VM.get(args.vm_id)
    print(vm)



# get VM from vm-name using pyvmomi
if args.vm_name:
    for vm in virtual_machines:
        if vm.name == args.vm_name:
            print(vm.summary.config)

# get VM from instance uuid using pyvmomi
if args.instance_uuid:
    vm = search_index.FindByUuid(instanceUuid=True, uuid=args.instance_uuid, vmSearch=True)
    if vm:
        print(vm.summary.config)

# get VM from bios uuid using pyvmomi
if args.bios_uuid:
    vm = search_index.FindByUuid(instanceUuid=False, uuid=args.bios_uuid, vmSearch=True)
    if vm:
        print(vm.summary.config)

if not vm:
    print("VM not found")