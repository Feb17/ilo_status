import redfish
import json

"""Get server health status via iLO RESTful API"""


def get_ilo_status(server_ip):

    # ip_list = 'https://10.109.23.144'  # ilo4
    username = "administrator"
    password = "to79dHSQ0fV5e8P"

    # Create a Redfish client object
    Redfish_Obj = redfish.redfish_client(base_url=server_ip, username=username, password=password)

    # Login to the server
    Redfish_Obj.login()

    # Get the server health status
    response = Redfish_Obj.get("/redfish/v1/Systems/1")
    system_info = response.dict

    # 最终展示的系统状态数据
    health_data = system_info['Oem']['Hpe']['AggregateHealthStatus']

    # 需要遍历查询的项目
    failure_dict = {}

    HostName = system_info['HostName']
    SerialNumber = system_info['SerialNumber']
    Model = system_info['Model']
    Status = system_info['Status']

    # Check overview health status
    for key, value in health_data.items():
        if isinstance(value, dict):
            if 'Health' in value['Status'] and value['Status']['Health'] not in ['OK', 'Ready', 'Redundant']:
                failure_dict[key] = value
        elif value not in ['OK', 'Ready', 'Redundant']:
            failure_dict[key] = value

    if failure_dict:
        print(failure_dict)
    else:
        print('System status all good!')

    # Check Fan status
    if 'Fans' in failure_dict.keys():  # 实际应用需要改为failure_dict
        fan_info_list = []
        fan_url = '/redfish/v1/Chassis/1/Thermal/'
        fan_rep = Redfish_Obj.get(fan_url).dict
        for fan in fan_rep['Fans']:
            fan_dict = {}
            fan_info = Redfish_Obj.get(fan['@odata.id']).dict
            fan_dict['Name'] = fan['Name']
            fan_dict['Status'] = fan['Status']['Health']
            fan_info_list.append(fan_dict)
        fans_dict = {'Fans': fan_info_list}
        health_data.update(fans_dict)

    # Check Memory status
    if 'Memory' in failure_dict.keys():  # 实际应用需要改为failure_dict
        mem_info_list = []
        mem_url = system_info['Memory']['@odata.id']
        mem_rep = Redfish_Obj.get(mem_url).dict
        for mem in mem_rep['Members']:
            mem_dict = {}
            mem_info = Redfish_Obj.get(mem['@odata.id']).dict
            mem_dict['DeviceLocator'] = mem_info['DeviceLocator']
            mem_dict['Status'] = mem_info['Status']['Health']
            mem_info_list.append(mem_dict)
        mems_dict = {'Memory': mem_info_list}
        health_data.update(mems_dict)

    # Check Network status
    if 'Network' in failure_dict.keys():  # 实际应用需要改为failure_dict
        net_info_list = []
        net_url = system_info['EthernetInterfaces']['@odata.id']
        net_rep = Redfish_Obj.get(net_url).dict
        for net in net_rep['Members']:
            net_dict = {}
            net_info = Redfish_Obj.get(net['@odata.id']).dict
            net_dict['Name'] = net_info['Name']
            net_dict['Status'] = net_info['Status']['Health']
            net_info_list.append(net_dict)
        nets_dict = {'Network': net_info_list}
        health_data.update(nets_dict)

    # Check disk status
    if 'Storage' in failure_dict.keys():  # 实际应用需要改为failure_dict
        disk_info_list = []
        disk_url = '/redfish/v1/Systems/1/SmartStorage/ArrayControllers/'
        disk_rep = Redfish_Obj.get(disk_url).dict
        for disk in disk_rep['Members']:
            disk_dict = {}
            disk_info = Redfish_Obj.get(disk['@odata.id']).dict
            disk_dict['Name'] = disk_info['Model']
            disk_dict['Status'] = disk_info['Status']['Health']
            disk_dict['CacheModuleStatus'] = disk_info['CacheModuleStatus']['Health']
            disk_info_list.append(disk_dict)
        disks_dict = {'Storage': disk_info_list}
        health_data.update(disks_dict)

    # Check CPU status
    if 'Processors' in failure_dict.keys():  # 实际应用需要改为failure_dict
        cpu_info_list = []
        processor_url = system_info['Processors']['@odata.id']
        processor_rep = Redfish_Obj.get(processor_url).dict
        for cpu in processor_rep['Members']:
            cpu_dict = {}
            processor_info = Redfish_Obj.get(cpu['@odata.id']).dict
            cpu_dict['Socket'] = processor_info['Socket']
            cpu_dict['Status'] = processor_info['Status']['Health']
            cpu_info_list.append(cpu_dict)
        cpus_dict = {'Processors': cpu_info_list}
        health_data.update(cpus_dict)

    # Check Power status
    if 'PowerSupplies' in failure_dict.keys():  # 实际应用需要改为failure_dict
        power_info_list = []
        power_url = '/redfish/v1/Chassis/1/Power/'
        power_rep = Redfish_Obj.get(power_url).dict
        for power in power_rep['PowerSupplies']:
            power_dict = {}
            power_dict['SerialNumber'] = power['SerialNumber']
            power_dict['SparePartNumber'] = power['SparePartNumber']
            power_dict['Status'] = power['Status']['Health']
            power_info_list.append(power_dict)
        powers_dict = {'PowerSupplies': power_info_list}
        health_data.update(powers_dict)

    # Logout from the server
    Redfish_Obj.logout()

    return health_data
