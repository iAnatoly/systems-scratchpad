"""
See https://docs.openstack.org/swift/latest/ring_background.html

"""

from hashlib import md5

NODE_COUNT = 100
DATA_ID_COUNT = 10000000
REPLICAS = 3
REPLICA_STEP = 5

node_counts = [0] * NODE_COUNT

print("Adding data to nodes: ", end='', flush=True)

for data_id in range(DATA_ID_COUNT):
    s_data_id = str(data_id).encode('utf8')

    hsh = int(md5(s_data_id).hexdigest(),16)
    node_id = hsh % NODE_COUNT
    node_counts[node_id] += 1

    for j in range(1,REPLICAS):
        node_counts[(node_id + j*REPLICA_STEP) % NODE_COUNT] += 1

    #progress bar, please ignore:
    if data_id % (DATA_ID_COUNT//20) == 0:
        print(".",end='', flush=True)

print(" Done.")
print(node_counts)

desired_count = (DATA_ID_COUNT / NODE_COUNT) * REPLICAS
print(f'{desired_count}: Desired data ids per node')
max_count = max(node_counts)
over = 100.0 * (max_count - desired_count) / desired_count
print(f'{max_count}: Most data ids on one node, {over} over')
min_count = min(node_counts)
under = 100.0 * (desired_count - min_count) / desired_count
print(f'{min_count}: Least data ids on one node, {under} under')
