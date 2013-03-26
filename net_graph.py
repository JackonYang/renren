# -*- coding: utf-8-*-
import pickle
import igraph

def init_graph(data, orig_id):
	friends=data[orig_id]
	print(data.keys())
	#print(friends.keys())
	g=igraph.Graph(len(friends))
	i=0
	for rid, name in friends.items():
		g.vs[i]['rid']=rid
		g.vs[i]['name']=name
		#print(name)
		i += 1
	#add edges
	for rid in g.vs['rid']:
		for fid in set(data.get(rid,dict()).keys())&set(friends.keys()):
			g.add_edges((g.vs['rid'].index(rid), g.vs['rid'].index(fid)))
	g.simplify()
	return g

def showGraph(graph,filename):
	ly=graph.layout('fr')
	visual_style = {}
	visual_style["vertex_size"] = 5
	visual_style['layout']=ly
	#visual_style["vertex_label"] = g.vs["uid"]
	#visual_style["vertex_label"] = graph.vs["name"]
	if filename is not None:
		igraph.plot(graph,"{}.png".format(filename),**visual_style)
	else:
		igraph.plot(graph,**visual_style)

friends=pickle.load(open('spread_friendList.p','rb'))
rid='498934189'

if __name__=='__main__':
	gg=init_graph(friends,rid)
	showGraph(gg,'pic')
