import sys
import xml.etree.cElementTree as ET
from xml.dom import expatbuilder

class Group:
    def __init__(self, group_id, group_label=None, group_description=None, group_url=None, group_color="#8AB339"):
        self.group_id = group_id

        if group_label:
            self.group_label = group_label
        else:
            self.group_label = group_id

        self.group_description = group_description
        self.group_url = group_url

        self.group_color = group_color

        self.nodes = {}
        self.groups = {}
        self.edges = {}

    def add_node(self, node_id, **kwargs):
        if node_id in self.nodes.keys():
            raise RuntimeWarning("Node %s already exists" % node_id)

        self.nodes[node_id] = Node("{}::{}".format(self.group_id, node_id), **kwargs)

    def add_group(self, group_id, **kwargs):
        if group_id in self.groups.keys():
            raise RuntimeWarning("Group %s already exists" % group_id)

        self.groups[group_id] = Group("{}::{}".format(self.group_id, group_id), **kwargs)

    def add_edge(self, edge_id, node1, node2, **kwargs):
        if edge_id in self.edges.keys():
            raise RuntimeWarning("Edge %s already exists" % edge_id)

        self.edges[edge_id] = Edge("{}::{}".format(self.group_id, edge_id), "{}::{}".format(self.group_id, node1), "{}::{}".format(self.group_id, node2), **kwargs)

    def generate_xml(self):
        node = ET.Element("node", id=str(self.group_id))
        node.set("yfiles.foldertype", "folder")

        if self.group_url:
            data_url = ET.SubElement(node, "data", key="d4")
            data_url.set("xml:space", "preserve")
            data_url.text = self.group_url

        if self.group_description:
            data_description = ET.SubElement(node, "data", key="d3")
            data_description.set("xml:space", "preserve")
            data_description.text = self.group_description

        data_node = ET.SubElement(node, "data", key="d5")
        y_ProxyAutoBoundsNode = ET.SubElement(data_node, "y:ProxyAutoBoundsNode")
        y_Realizers = ET.SubElement(y_ProxyAutoBoundsNode, "y:Realizers", active="1")

        y_GenericGroupNode = ET.SubElement(y_Realizers, "y:GenericGroupNode", configuration="PanelNode")
        y_Geometry = ET.SubElement(y_GenericGroupNode, "y:Geometry", height="100", width="100", x="0", y="0")
        y_Fill = ET.SubElement(y_GenericGroupNode, "y:Fill", color=self.group_color, transparent="false")
        y_BorderStyle = ET.SubElement(y_GenericGroupNode, "y:BorderStyle", hasColor="false", type="line", width="1.0")
        y_NodeLabel = ET.SubElement(y_GenericGroupNode, "y:NodeLabel", alignment="center", autoSizePolicy="content", borderDistance="0.0", fontFamily="Dialog", fontSize="24",
                                    fontStyle="plain", hasBackgroundColor="false", hasLineColor="false", height="0", horizontalTextPosition="center",
                                    iconTextGap="4", modelName="internal", modelPosition="t", textColor="#000000", verticalTextPosition="bottom", visible="true",
                                    width="0", x="0", y="0.0")
        y_NodeLabel.set("xml:space", "preserve")
        y_NodeLabel.text = self.group_label
        y_StyleProperties = ET.SubElement(y_GenericGroupNode, "y:StyleProperties")
        y_Property = ET.SubElement(y_StyleProperties, "y:Property", name="headerBackground", value=self.group_color)
        y_Property.set("class", "java.awt.Color")
        y_State = ET.SubElement(y_GenericGroupNode, "y:State", autoResize="true", closed="false", closedHeight="50.0", closedWidth="50.0")
        y_Insets = ET.SubElement(y_GenericGroupNode, "y:Insets", bottom="15", bottomF="15.0", left="15", leftF="15.0", right="15", rightF="15.0", top="15", topF="15.0")
        y_BorderInsets = ET.SubElement(y_GenericGroupNode, "y:BorderInsets", bottom="0", bottomF="0.0", left="0", leftF="0.0", right="0", rightF="0.0", top="0", topF="0.0")

        y_GenericGroupNode = ET.SubElement(y_Realizers, "y:GenericGroupNode", configuration="PanelNode")
        y_Geometry = ET.SubElement(y_GenericGroupNode, "y:Geometry", height="100", width="100", x="0", y="0")
        y_Fill = ET.SubElement(y_GenericGroupNode, "y:Fill", color=self.group_color, transparent="false")
        y_BorderStyle = ET.SubElement(y_GenericGroupNode, "y:BorderStyle", hasColor="false", type="line", width="1.0")
        y_NodeLabel = ET.SubElement(y_GenericGroupNode, "y:NodeLabel", alignment="node_size", autoSizePolicy="node_size", borderDistance="0.0", fontFamily="Dialog", fontSize="24",
                                    fontStyle="plain", hasBackgroundColor="false", hasLineColor="false", height="0", horizontalTextPosition="center",
                                    iconTextGap="4", modelName="internal", modelPosition="c", textColor="#000000", verticalTextPosition="bottom", visible="true",
                                    width="0", x="0", y="0.0")
        y_NodeLabel.set("xml:space", "preserve")
        y_NodeLabel.text = self.group_label
        y_StyleProperties = ET.SubElement(y_GenericGroupNode, "y:StyleProperties")
        y_Property = ET.SubElement(y_StyleProperties, "y:Property", name="headerBackground", value=self.group_color)
        y_Property.set("class", "java.awt.Color")
        y_State = ET.SubElement(y_GenericGroupNode, "y:State", autoResize="true", closed="true", closedHeight="50.0", closedWidth="50.0")
        y_Insets = ET.SubElement(y_GenericGroupNode, "y:Insets", bottom="15", bottomF="15.0", left="15", leftF="15.0", right="15", rightF="15.0", top="15", topF="15.0")
        y_BorderInsets = ET.SubElement(y_GenericGroupNode, "y:BorderInsets", bottom="0", bottomF="0.0", left="0", leftF="0.0", right="0", rightF="0.0", top="0", topF="0.0")

        graph_node = ET.SubElement(node, "graph", edgedefault="directed", id="{}:".format(self.group_id))

        for node_id in self.nodes:
            node_xml = self.nodes[node_id].generate_xml()
            graph_node.append(node_xml)

        for group_id in self.groups:
            group_xml = self.groups[group_id].generate_xml()
            graph_node.append(group_xml)

        for edge_id in self.edges:
            edge_xml = self.edges[edge_id].generate_xml()
            graph_node.append(edge_xml)

        return node

class Node:
    def __init__(self, node_id, node_label=None, node_description=None, node_url=None, 
                 node_height="100", node_width="100", node_x="0", node_y="0", 
                 node_color="#0275D4", node_border_color="#0275D4", node_border_width="1", 
                 node_label_color="#000000"):
        self.node_id = node_id

        if node_label:
            self.node_label = node_label
        else:
            self.node_label = node_id

        self.node_description = node_description

        self.node_url = node_url

        self.geom = {}
        self.geom["height"] = node_height
        self.geom["width"] = node_width
        self.geom["x"] = node_x
        self.geom["y"] = node_y

        self.node_color = node_color
        self.node_border_color = node_border_color
        self.node_border_width = node_border_width

        self.node_label_color = node_label_color

    def generate_xml(self):
        node = ET.Element("node", id=str(self.node_id))

        if self.node_url:
            data_url = ET.SubElement(node, "data", key="d4")
            data_url.set("xml:space", "preserve")
            data_url.text = self.node_url

        if self.node_description:
            data_description = ET.SubElement(node, "data", key="d3")
            data_description.set("xml:space", "preserve")
            data_description.text = self.node_description

        data_node = ET.SubElement(node, "data", key="d5")
        y_ShapeNode = ET.SubElement(data_node, "y:ShapeNode")
        y_Geometry = ET.SubElement(y_ShapeNode, "y:Geometry", height=self.geom["height"], width=self.geom["width"], x=self.geom["x"], y=self.geom["y"])
        y_Fill = ET.SubElement(y_ShapeNode, "y:Fill", color=self.node_color, transparent="false")
        y_BorderStyle = ET.SubElement(y_ShapeNode, "y:BorderStyle", cap="0", color=self.node_border_color, dashPhase="0.0", join="0", 
                                      miterLimit="10.0", raised="false", type="custom", width=self.node_border_width)
        y_NodeLabel = ET.SubElement(y_ShapeNode, "y:NodeLabel", alignment="center", autoSizePolicy="content", fontFamily="'Arial'", 
                                    fontSize="24", fontStyle="plain", hasBackgroundColor="false", hasLineColor="false", height="50", 
                                    horizontalTextPosition="center", iconTextGap="4", modelName="custom", textColor=self.node_label_color, verticalTextPosition="bottom", 
                                    visible="true", width="50", x="0", y="50")
        y_NodeLabel.set("xml:space", "preserve")
        y_NodeLabel.text = self.node_label
        y_Shape = ET.SubElement(y_ShapeNode, "y:Shape", type="roundrectangle")

        return node

class Edge:
    def __init__(self, edge_id, node1, node2, edge_description=None, edge_color="#000000", edge_width="1"):
        self.edge_id = edge_id

        self.node1 = node1
        self.node2 = node2

        self.edge_description = edge_description

        self.edge_color = edge_color
        self.edge_width = edge_width

    def generate_xml(self):
        edge = ET.Element("edge", id=str(self.edge_id), source=str(self.node1), target=str(self.node2))

        if self.edge_description:
            data_description = ET.SubElement(edge, "data", key="d8")
            data_description.set("xml:space", "preserve")
            data_description.text = self.edge_description

        data_edge = ET.SubElement(edge, "data", key="d9")
        y_PolyLineEdge = ET.SubElement(data_edge, "y:PolyLineEdge")
        y_Path = ET.SubElement(y_PolyLineEdge, "y:Path", sx="0.0", sy="0.0", tx="0.0", ty="0.0")
        y_LineStyle = ET.SubElement(y_PolyLineEdge, "y:LineStyle", color=self.edge_color, type="line", width=self.edge_width)
        y_Arrows = ET.SubElement(y_PolyLineEdge, "y:Arrows", source="none", target="standard")
        y_BendStyle = ET.SubElement(y_PolyLineEdge, "y:BendStyle", smoothed="false")

        return edge

class Graph:
    def __init__(self, directed="directed", graph_id="G"):
        self.nodes = {}
        self.edges = {}
        self.groups = {}

        self.directed = directed
        self.graph_id = graph_id

        self.graphml = ""

    def generate_graphml(self):

        graphml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
        graphml.set("xmlns:java", "http://www.yworks.com/xml/yfiles-common/1.0/java")
        graphml.set("xmlns:sys", "http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0")
        graphml.set("xmlns:x", "http://www.yworks.com/xml/yfiles-common/markup/2.0")
        graphml.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        graphml.set("xmlns:y", "http://www.yworks.com/xml/graphml")
        graphml.set("xmlns:yed", "http://www.yworks.com/xml/yed/3")
        graphml.set("xsi:schemaLocation", "http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd")

        node_key = ET.SubElement(graphml, "key", id="d0")
        node_key.set("for", "port")
        node_key.set("yfiles.type", "portgraphics")

        node_key = ET.SubElement(graphml, "key", id="d1")
        node_key.set("for", "port")
        node_key.set("yfiles.type", "portgeometry")

        node_key = ET.SubElement(graphml, "key", id="d2")
        node_key.set("for", "port")
        node_key.set("yfiles.type", "portuserdata")

        node_key = ET.SubElement(graphml, "key", id="d3")
        node_key.set("for", "node")
        node_key.set("attr.name", "description")
        node_key.set("attr.type", "string")

        node_key = ET.SubElement(graphml, "key", id="d4")
        node_key.set("for", "node")
        node_key.set("attr.name", "url")
        node_key.set("attr.type", "string")

        node_key = ET.SubElement(graphml, "key", id="d5")
        node_key.set("for", "node")
        node_key.set("yfiles.type", "nodegraphics")

        node_key = ET.SubElement(graphml, "key", id="d6")
        node_key.set("for", "graphml")
        node_key.set("yfiles.type", "resources")

        node_key = ET.SubElement(graphml, "key", id="d7")
        node_key.set("for", "edge")
        node_key.set("attr.name", "url")
        node_key.set("attr.type", "string")

        node_key = ET.SubElement(graphml, "key", id="d8")
        node_key.set("for", "edge")
        node_key.set("attr.name", "description")
        node_key.set("attr.type", "string")

        node_key = ET.SubElement(graphml, "key", id="d9")
        node_key.set("for", "edge")
        node_key.set("yfiles.type", "edgegraphics")

        graph = ET.SubElement(graphml, "graph", edgedefault=self.directed, id=self.graph_id)

        for node_id in self.nodes:
            node_xml = self.nodes[node_id].generate_xml()
            graph.append(node_xml)

        for group_id in self.groups:
            group_xml = self.groups[group_id].generate_xml()
            graph.append(group_xml)

        for edge_id in self.edges:
            edge_xml = self.edges[edge_id].generate_xml()
            graph.append(edge_xml)

        data_resources = ET.SubElement(graphml, "data", key="d6")
        y_Resources = ET.SubElement(data_resources, "y:Resources")

        self.graphml = graphml

    def add_node(self, node_id, **kwargs):
        if node_id in self.nodes.keys():
            raise RuntimeWarning("Node %s already exists" % node_id)

        self.nodes[node_id] = Node(node_id, **kwargs)

    def add_edge(self, edge_id, node1, node2, **kwargs):
        if edge_id in self.edges.keys():
            raise RuntimeWarning("Edge %s already exists" % edge_id)

        self.edges[edge_id] = Edge(edge_id, node1, node2, **kwargs)

    def add_group(self, group_id, **kwargs):
        if group_id in self.groups.keys():
            raise RuntimeWarning("Group %s already exists" % group_id)

        self.groups[group_id] = Group(group_id, **kwargs)

    def write_graph(self, filename):
        self.generate_graphml()

        graph_xml = ET.tostring(self.graphml, encoding='UTF-8', method='xml').decode('UTF-8')

        dom = expatbuilder.parseString(graph_xml, False)
        pretty_xml_as_string = dom.toprettyxml()

        f = open(filename, "w")
        f.write(pretty_xml_as_string)
        f.close()
    
