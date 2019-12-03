# coding: utf-8
# File: GraphShow.py
# Date: 19-12-03

'''创建展示页面'''
class GraphShow():
    '''读取文件数据'''
    def create_page(self, events):
        nodes = []
        for event in events:
            if event[0] not in nodes:
                nodes.append(event[0])
            if event[1] not in nodes:
                nodes.append(event[1])
        node_dict = {node: index for index, node in enumerate(nodes)}

        data_nodes = []
        data_edges = []
        for node, id in node_dict.items():
            data = {}
            data["group"] = 'Event'
            data["id"] = id
            data["label"] = node
            data_nodes.append(data)

        for edge in events:
            data = {}
            data['from'] = node_dict.get(edge[0])
            data['label'] = ''
            data['to'] = node_dict.get(edge[1])
            data_edges.append(data)
        return data_nodes, data_edges

