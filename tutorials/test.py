import os
import sys
nb_dir = os.path.split(os.getcwd())[0]
if nb_dir not in sys.path:
    sys.path.append(nb_dir)

#import os
import csv
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from timeseries.strategies import TimeseriesToGraphStrategy, TimeseriesEdgeVisibilityConstraintsNatural, TimeseriesEdgeVisibilityConstraintsHorizontal, EdgeWeightingStrategyNull, TimeseriesEdgeVisibilityConstraintsVisibilityAngle
from generation.strategies import RandomWalkWithRestartSequenceGenerationStrategy, RandomWalkSequenceGenerationStrategy, RandomNodeSequenceGenerationStrategy, RandomNodeNeighbourSequenceGenerationStrategy, RandomDegreeNodeSequenceGenerationStrategy
from core import model 
from sklearn.model_selection import train_test_split
import itertools

import xml.etree.ElementTree as ET
import random
import hashlib

import csv_read
import xml_read
import graph_strategy
import graph
import link
import ts_process_strategy
import ts_to_graph


amazon_path = os.path.join(os.getcwd(), "amazon", "AMZN.csv")
apple_path = os.path.join(os.getcwd(), "apple", "APPLE.csv")

ts_to_graph.TimeSeriesToGraph()\
    .from_csv(csv_read.CsvStock(amazon_path, "Close"))\
    .process(ts_process_strategy.Segment(60, 90))\
    .to_graph(graph_strategy.NaturalVisibility().with_limit(1))\
    .add_edge(0,2)\
    .add_edge(13, 21, weight = 17)\
    .link(link.Link().by_value(link.SameValue(2)).seasonalities(15))\
    .draw("blue")


#--------------------------------------------------------------------------------

ts_to_graph.TimeSeriesToGraph()\
    .from_csv(csv_read.CsvStock(apple_path, "Close"))\
    .process(ts_process_strategy.Segment(60, 120))\
    .process(ts_process_strategy.SlidingWindow(5))\
    .to_graph(graph_strategy.NaturalVisibility())\
    .combine_identical_nodes()\
    .draw("red")

#--------------------------------------------------------------------------------


a = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(amazon_path, "Close"))\
    .process(ts_process_strategy.Segment(60, 80))\
    .to_graph(graph_strategy.NaturalVisibility())\
    .link(link.Link().by_value(link.SameValue(1)))

b = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(apple_path, "Close"))\
    .process(ts_process_strategy.Segment(120, 140))\
    .to_graph(graph_strategy.NaturalVisibility().with_limit(1))

c = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(amazon_path, "Close"))\
    .process(ts_process_strategy.Segment(180, 200))\
    .to_graph(graph_strategy.NaturalVisibility().with_angle(120))\
    .combine_identical_nodes()

d = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(apple_path, "Close"))\
    .process(ts_process_strategy.Segment(240, 260))\
    .to_graph(graph_strategy.NaturalVisibility())\
    .link(link.Link().seasonalities(15))

i = ts_to_graph.MultivariateTimeSeriesToGraph()\
    .add(a)\
    .add(b)\
    .add(c)\
    .add(d)\
    .link(link.Link().time_coocurence())\
    .link(link.Link().by_value(link.SameValue(0.5)))\
    .combine_identical_nodes()\
    .draw("purple")  

#-------------------------------------------------------------------------------

x = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(amazon_path, "Close"))\
    .process(ts_process_strategy.Segment(60, 90))\
    .process(ts_process_strategy.SlidingWindow(5))\
    .to_graph(graph_strategy.NaturalVisibility())\
    .combine_identical_nodes()


y = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(apple_path, "Close"))\
    .process(ts_process_strategy.Segment(120, 150))\
    .process(ts_process_strategy.SlidingWindow(5))\
    .to_graph(graph_strategy.NaturalVisibility())\
    .combine_identical_nodes()

z = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(amazon_path, "Close"))\
    .process(ts_process_strategy.Segment(180, 210))\
    .process(ts_process_strategy.SlidingWindow(5))\
    .to_graph(graph_strategy.NaturalVisibility())

w = ts_to_graph.TimeSeriesToGraph().from_csv(csv_read.CsvStock(apple_path, "Close"))\
    .process(ts_process_strategy.Segment(240, 270))\
    .process(ts_process_strategy.SlidingWindow(5))\
    .to_graph(graph_strategy.NaturalVisibility())\
    .combine_identical_nodes()

j = ts_to_graph.MultivariateTimeSeriesToGraph()\
    .add(x)\
    .add(y)\
    .add(z)\
    .add(w)\
    .link(link.Link(multi=True).time_coocurence())\
    .combine_identical_nodes()\
    .draw("red")

#------------------------------------------------------------------------------------

graph.Graph(a.return_graph())\
    .set_nodes(i.return_graph().nodes, i.return_graph().nodes(data=True))\
    .walk_through_all()\
    .choose_next_node("weighted")\
    .choose_next_value("sequential")\
    .skip_every_x_steps(1)\
    .ts_length(100)\
    .to_time_sequence()\
    .draw()

#----------------------------------------------------------------------------------

graph.GraphSlidWin(x.return_graph())\
    .set_nodes(x.return_graph().nodes)\
    .choose_next_node("weighted")\
    .choose_next_value("random")\
    .skip_every_x_steps(1)\
    .ts_length(50)\
    .to_time_sequence()\
    .draw()

#---------------------------------------------------------------------------------

graph.Graph(i.return_graph())\
    .set_nodes(i.get_graph_nodes(), i.get_graph_nodes_data())\
    .walk_through_all()\
    .change_graphs_every_x_steps(2)\
    .choose_next_node("random")\
    .choose_next_value("sequential")\
    .skip_every_x_steps(1)\
    .ts_length(50)\
    .to_multiple_time_sequences()\
    .draw()

#-------------------------------------------------------------------------------

graph.GraphSlidWin(j.return_graph())\
    .set_nodes(j.get_graph_nodes())\
    .choose_next_node("weighted")\
    .choose_next_value("sequential")\
    .skip_every_x_steps(0)\
    .ts_length(100)\
    .to_multiple_time_sequences()\
    .draw()

