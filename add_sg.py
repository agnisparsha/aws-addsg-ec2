#!/usr/bin/python

__author__ = 'agnisparsha'

import requests
from boto.ec2.connection import EC2Connection


AWS_ACCESS_KEY_ID = '<access_key_id>'
AWS_SECRET_ACCESS_KEY = '<access_secret_key>'
AWS_REGION = '<eg,. us-east-1c>'


def get_my_ip():
	request = requests.get(r'http://jsonip.com')
	ip = request.json()['ip']
	return ip

def create_connection():
	conn = EC2Connection (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	return conn

def get_instances(conn):
	instances = conn.get_all_instances()
	return instances

def print_instances(inst_array):
	index = 0
	for isntance in inst_array:
		print '%d. %s' % (index, isntance)
		index += 1

def get_sg_print(instance):
	sg_array = instance.groups
	index = 0
	for sg in sg_array:
		print '%d. Name: %s' % (index, sg.name)
	return sg_array


if __name__ == '__main__':
	# Create Connection
	connection = create_connection()
	instances = get_instances(connection)
	print_instances(instances)
	chosen_instance = int(raw_input('Choose Instance: '))
	instance_obj = instances[chosen_instance]

	# Get the instance group
	sgs = get_sg_print(instance_obj)
	
	
	sg_chosen_num = int(raw_input('Choose SG: '))
	sg_chosen = sgs[sg_chosen_num]

	# Choose the security group from the isntance group name
	groups = [sg for sg in connection.get_all_security_groups() if sg.name == sg_chosen.name]
	group = groups[0] if groups else None
	
	from_port = int(raw_input('From Port: '))
	to_port = int(raw_input('To Port: '))
	my_ip = get_my_ip()
	cidr = '%s0/24' % my_ip[:-len(my_ip.split('.')[-1])]

	# Add the rule by authorizing it
	group.authorize(ip_protocol='tcp', from_port=from_port,
		to_port=to_port, cidr_ip=cidr)

