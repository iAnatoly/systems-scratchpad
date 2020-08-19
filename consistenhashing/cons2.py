"""
See https://docs.openstack.org/swift/latest/ring_background.html

"""
from hashlib import md5

NODE_COUNT = 100
DATA_ID_COUNT = 10000000
VNODE_COUNT = 1000

vnode2node = []
for vnode_id in range(VNODE_COUNT):
    vnode2node.append(vnode_id % NODE_COUNT)

new_vnode2node = vnode2node.copy()

new_node_id = NODE_COUNT
vnodes_to_reassign = VNODE_COUNT / (NODE_COUNT + 1)

while vnodes_to_reassign > 0:
    for node_to_take_from in range(NODE_COUNT):
        for vnode_id, node_id in enumerate(vnode2node):
            if node_id == node_to_take_from:
                vnode2node[vnode_id] = new_node_id
                vnodes_to_reassign -= 1
                break
        if vnodes_to_reassign <= 0:
            break

moved_ids = 0
for data_id in range(DATA_ID_COUNT):
    hsh = int(md5(str(data_id).encode('utf8')).hexdigest(),16)
    vnode_id = hsh % VNODE_COUNT
    node_id = vnode2node[vnode_id]
    new_node_id = new_vnode2node[vnode_id]
    if node_id != new_node_id:
        moved_ids += 1

percent_moved = 100.0 * moved_ids / DATA_ID_COUNT
print(f'{moved_ids} ids moved, {percent_moved}%')
