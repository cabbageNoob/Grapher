# coding: utf-8
# File: GraphShow.py
# Date: 19-12-03

'''创建展示页面'''
class GraphShow():
    def __init__(self):
        self.base = '''
    <html>
    <head>
      <script type="text/javascript" src="VIS/dist/vis.js"></script>
      <link href="VIS/dist/vis.css" rel="stylesheet" type="text/css">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>

    <div id="VIS_draw"></div>

    <script type="text/javascript">
      var network;
      var allNodes;
      var highlightActive = false;
    
      var nodesDataset = new vis.DataSet(data_nodes); 
      var edgesDataset = new vis.DataSet(data_edges); 

      var container = document.getElementById("VIS_draw");

      var data = {
        nodes: nodesDataset,
        edges: edgesDataset
      };
      var options = {
          nodes: {
            shape: 'circle',
            size: 15,
              font: {
                  size: 15
              }
          },
          edges: {
             font: {
                  size: 10,
                  align: 'center'
              },
              color: 'red',
              arrows: {
                  to: {enabled: true, scaleFactor: 1.2}
              },
              smooth: {enabled: true}
          },
          physics: true,
          interaction: {
            tooltipDelay: 200,
            //hideEdgesOnDrag: true,
            //hideEdgesOnZoom: true,
          }
      };
    
      network = new vis.Network(container, data, options);
      // get a JSON object
      allNodes = nodesDataset.get({returnType:"Object"});
      network.on("click",neighbourhoodHighlight);
      
      function neighbourhoodHighlight(params) {
            // if something is selected:
            if (params.nodes.length > 0) {
              highlightActive = true;
              var i,j;
              var selectedNode = params.nodes[0];
              var degrees = 2;

              // mark all nodes as hard to read.
              for (var nodeId in allNodes) {
                allNodes[nodeId].color = 'rgba(200,200,200,0.5)';
                if (allNodes[nodeId].hiddenLabel === undefined) {
                  allNodes[nodeId].hiddenLabel = allNodes[nodeId].label;
                  allNodes[nodeId].label = undefined;
                }
              }
              var connectedNodes = network.getConnectedNodes(selectedNode);
              var allConnectedNodes = [];

              // get the second degree nodes
              for (i = 1; i < degrees; i++) {
                for (j = 0; j < connectedNodes.length; j++) {
                  allConnectedNodes = allConnectedNodes.concat(network.getConnectedNodes(connectedNodes[j]));
                }
              }

              // all second degree nodes get a different color and their label back
              for (i = 0; i < allConnectedNodes.length; i++) {
                allNodes[allConnectedNodes[i]].color = 'rgba(150,150,150,0.75)';
                if (allNodes[allConnectedNodes[i]].hiddenLabel !== undefined) {
                  allNodes[allConnectedNodes[i]].label = allNodes[allConnectedNodes[i]].hiddenLabel;
                  allNodes[allConnectedNodes[i]].hiddenLabel = undefined;
                }
              }

              // all first degree nodes get their own color and their label back
              for (i = 0; i < connectedNodes.length; i++) {
                allNodes[connectedNodes[i]].color = undefined;
                if (allNodes[connectedNodes[i]].hiddenLabel !== undefined) {
                  allNodes[connectedNodes[i]].label = allNodes[connectedNodes[i]].hiddenLabel;
                  allNodes[connectedNodes[i]].hiddenLabel = undefined;
                }
              }

              // the main node gets its own color and its label back.
              allNodes[selectedNode].color = undefined;
              if (allNodes[selectedNode].hiddenLabel !== undefined) {
                allNodes[selectedNode].label = allNodes[selectedNode].hiddenLabel;
                allNodes[selectedNode].hiddenLabel = undefined;
              }
            }
            else if (highlightActive === true) {
              // reset all nodes
              for (var nodeId in allNodes) {
                allNodes[nodeId].color = undefined;
                if (allNodes[nodeId].hiddenLabel !== undefined) {
                  allNodes[nodeId].label = allNodes[nodeId].hiddenLabel;
                  allNodes[nodeId].hiddenLabel = undefined;
                }
              }
              highlightActive = false
            }

            // transform the object into an array
            var updateArray = [];
            for (nodeId in allNodes) {
              if (allNodes.hasOwnProperty(nodeId)) {
                updateArray.push(allNodes[nodeId]);
              }
            }
            nodesDataset.update(updateArray);
          }
    </script>
    </body>
    </html>
    '''
    '''读取文件数据'''
    def create_page(self, events):
        nodes = []
        for event in events:
            nodes.append(event[0])
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
        # self.create_html(data_nodes, data_edges)
        # return

    '''生成html文件'''
    def create_html(self, data_nodes, data_edges):
        f = open('graph_show.html', 'w+',encoding = 'utf8')
        html = self.base.replace('data_nodes', str(data_nodes)).replace('data_edges', str(data_edges))
        f.write(html)
        f.close()
