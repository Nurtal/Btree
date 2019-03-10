




class gate_frame(object):

	def __init__(self):
		self.name = None
		self.population = {}
		self.root = None
		self.parameters = []


class cell_population(object):

	def __init__(self):
		self.name = None
		self.gate_name = None
		self.id = None
		self.variables = {}
		self.root_id = None
		self.channels = []






## PANEL 1 POP ROOT STRUCTURE
panel_1_pop_id_to_root = {1:None,2:1,3:None,4:None,5:4,6:5,7:6,8:7,9:7,10:7,11:10,12:10,13:8,14:13,15:8,16:15,17:16,18:16,19:16,20:9,21:9,22:21,23:21,24:21,25:21,26:21,27:9,28:9,29:27,30:27}





def compute_back_frequency(gate, pop_name):
	"""
	-> compute frequency for a pop_name back to
	the root of the tree
	"""

	freq = gate.population[pop_name]

	while(gate.root != None):
		gate = gate.root
		freq = freq*gate.population[pop_name]

	return freq




def trace_tree(set_of_gate_frame):
	"""
	IN PROGRESS
	"""

	## importation
	import pydot

	## parameters
	frame_to_child = {}
	root_frame_name = "NA"
	already_plot = []
	node_to_plot = []

	## create the structure
	for gf in set_of_gate_frame:

		node_to_plot.append(gf.name)

		if(gf.root != None):

			if(gf.root.name not in frame_to_child.keys()):
				frame_to_child[str(gf.root.name)] = [gf.name]
			else:
				frame_to_child[str(gf.root.name)].append(gf.name)
		else:
			root_frame_name = gf.name

	## TODO : Display structure

	return frame_to_child

	

def get_pop_number(pop_name):
	"""
	"""

	## importation
	import pandas as pd

	## parameters
	data_file = "panel_1_pop_map.csv"
	good_number = "NA"

	## fetch good number
	dataset = open(data_file, "r")
	for line in dataset:
		line = line.rstrip()
		line_in_array = line.split(",")
		pop_number = line_in_array[0]
		test_name = line_in_array[1]

		if(test_name == pop_name):
			good_number = pop_number

	dataset.close()

	## return the pop number
	return good_number


def get_pop_name(pop_number):
	"""
	"""

	## importation
	import pandas as pd

	## parameters
	data_file = "panel_1_pop_map.csv"
	good_name = "NA"

	## fetch good number
	dataset = open(data_file, "r")
	for line in dataset:
		line = line.rstrip()
		line_in_array = line.split(",")
		test_number = line_in_array[0]
		pop_name = line_in_array[1]

		if(str(test_number) == str(pop_number)):

			good_name_in_array = pop_name.split("_CONCENTRATION")
			if(len(good_name_in_array) > 1):
				good_name = good_name_in_array[0]
				break
			else:
				good_name_in_array = pop_name.split("_FREQUENCY")
				if(len(good_name_in_array) > 1):
					good_name = good_name_in_array[0]
					break

	dataset.close()

	## return the pop number
	return good_name


def get_gate_name(pop_number):
	"""
	"""

	## parameters
	data_file = "panel_1_map.csv"
	gate_name = "NA"

	## fetch good number
	dataset = open(data_file, "r")
	for line in dataset:
		line = line.rstrip()
		line_in_array = line.split(",")
		test_number = line_in_array[0]
		pop_name = line_in_array[1]

		if(str(test_number) == str(pop_number)):
			gate_name = pop_name 

	dataset.close()

	## return the pop number
	return gate_name



def get_root(pop_id):
	"""
	"""

	return panel_1_pop_id_to_root[pop_id]



def get_frequencies(origin, target, panel_pop_structure):
	"""
	"""

	## parameters
	reach_target = False
	values_to_target = []
	
	origin_pop = panel_pop_structure[origin]
	print(origin_pop.variables)

	## get FREQUENCIES
	while(not reach_target):
		for var_name in origin_pop.variables.keys():
			var_name_in_array = var_name.split("_FREQUENCY_in ")
			if(len(var_name_in_array) > 1):
				
				back_pop = panel_pop_structure[origin_pop.root_id]

				back_variable = var_name_in_array[1]
				print(back_pop.name)
				if(back_pop.name == back_variable or back_pop.gate_name == back_variable):
					values_to_target.append(var_name)

				if(origin_pop.root_id == target):
					reach_target = True
				else:
					origin_pop = back_pop

	print(values_to_target)




def get_variables(pop_id):
	"""
	"""

	## parameters
	data_file = "panel_1_pop_map.csv"
	variables_list = []

	dataset = open(data_file, "r")
	for line in dataset:
		line = line.rstrip()
		line_in_array = line.split(",")
		pop_number = line_in_array[0]
		var_name = line_in_array[1]

		if(str(pop_id) == str(pop_number)):
			variables_list.append(var_name)

	dataset.close()

	return variables_list


def create_population_structure(pop_id):
	"""
	Instanciate a cell populations with it's
	pop id.
	"""

	## Instanciate cell populations
	cell_pop = cell_population()
	cell_pop.id = pop_id 
	cell_pop.name = get_pop_name(pop_id)
	cell_pop.gate_name = get_gate_name(pop_id)
	cell_pop.root_id = get_root(pop_id)

	## get variables
	variables = get_variables(pop_id)
	for var in variables:
		cell_pop.variables[var] = "NA"

	## return population object
	return cell_pop



def create_panel_1_populations():
	"""
	"""

	## parameters
	cell_structure = {}

	for x in range(1,31):
		cell_pop = create_population_structure(x)
		cell_structure[x] = cell_pop

	return cell_structure



def create_panel_1_structure():
	""" 
	Build a panel 1 structure and return a list of
	gate frame.


	TODO:
		- assign pop Leukocytes_CONCENTRATION_
		- assign pop PBMC_FREQUENCY_in Leukocytes
		- assign pop CD3pos_Tcells_FREQUENCY_in Leukocytes
		- assign pop CD3pos_Tcells_FREQUENCY_in PBMC
		- assign pop Monocytes_FREQUENCY_in Leukocytes
		- assign pop Monocytes_FREQUENCY_in PBMC
		- assign pop Lymphocytes_FREQUENCY_in Leukocytes
		- assign pop Lymphocytes_FREQUENCY_in PBMC
		- assign pop PMN_FREQUENCY_in Leukocytes
	"""



	## parameters
	bag_of_frame = []

	## NOT BEADS gate frame.
	gate_frame_not_beads = gate_frame()
	gate_frame_not_beads.name = "NOT BEADS"
	gate_frame_not_beads.population["pop3"] = "NA"
	gate_frame_not_beads.population["S1"] = "NA"
	gate_frame_not_beads.parameters = ["FSC-W","FSC-A"]
	bag_of_frame.append(gate_frame_not_beads)

	## S1 gate frame.
	gate_frame_S1 = gate_frame()
	gate_frame_S1.name = "S1"
	gate_frame_S1.root = gate_frame_not_beads
	gate_frame_S1.population["S2"] = "NA"
	gate_frame_S1.parameters = ["SSC-W","SSC-A"]
	bag_of_frame.append(gate_frame_S1)

	## S2 gate frame.
	gate_frame_S2 = gate_frame()
	gate_frame_S2.name = "S2"
	gate_frame_S2.root = gate_frame_S1
	gate_frame_S2.population["S3"] = "NA"
	gate_frame_S2.parameters = ["FSC-H","FSC-A"]
	bag_of_frame.append(gate_frame_S2)

	## S3 gate frame.
	gate_frame_S3 = gate_frame()
	gate_frame_S3.name = "S3"
	gate_frame_S3.root = gate_frame_S2
	gate_frame_S3.population["S3"] = "NA"
	gate_frame_S3.parameters = ["SSC-H","SSC-A"]
	bag_of_frame.append(gate_frame_S3)

	## S4 gate frame.
	gate_frame_S4 = gate_frame()
	gate_frame_S4.name = "S4"
	gate_frame_S4.root = gate_frame_S3
	gate_frame_S4.population["ALIVE"] = "NA"
	gate_frame_S4.population["Lymphocytes_CONCENTRATION_"] = "NA"
	gate_frame_S4.parameters = ["SSC-A","FSC-A"]
	bag_of_frame.append(gate_frame_S4)

	## S4-bis gate frame.
	gate_frame_S4bis = gate_frame()
	gate_frame_S4bis.name = "S4bis"
	gate_frame_S4bis.root = gate_frame_S3
	gate_frame_S4bis.population["GR COMPARTMENT"] = "NA"
	gate_frame_S4bis.parameters = ["SSC-A","CD15-PEA"]
	bag_of_frame.append(gate_frame_S4bis)

	## GR COMPARTMENT gate frame.
	gate_frame_gr_compartment = gate_frame()
	gate_frame_gr_compartment.name = "GR COMPARTMENT"
	gate_frame_gr_compartment.root = gate_frame_S4bis
	gate_frame_gr_compartment.population["CD15lowCD16high_Neutrophils_CONCENTRATION_"] = "NA"
	gate_frame_gr_compartment.population["CD15highCD16neg_Eosinophils_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_gr_compartment.population["CD15highCD16neg_Eosinophils_FREQUENCY_in PMN"] = "NA"
	gate_frame_gr_compartment.population["CD15lowCD16high_Neutrophils_FREQUENCY_in PMN"] = "NA"
	gate_frame_gr_compartment.parameters = ["CD16 FITC-A","CD15 PE-A"]
	bag_of_frame.append(gate_frame_gr_compartment)

	## ALIVE bis gate frame.
	gate_frame_alive_bis = gate_frame()
	gate_frame_alive_bis.name = "ALIVEbis"
	gate_frame_alive_bis.root = gate_frame_S4
	gate_frame_alive_bis.population["PBMC_CONCENTRATION_"] = "NA"
	gate_frame_alive_bis.parameters = ["SSC-A","FSC-A"]
	bag_of_frame.append(gate_frame_alive_bis)

	## PBMC gate frame.
	gate_frame_PBMC = gate_frame()
	gate_frame_PBMC.name = "PBMC"
	gate_frame_PBMC.root = gate_frame_alive_bis
	gate_frame_PBMC.population["CD15posCD14low_LDGs_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_PBMC.population["CD15posCD14low_LDGs_FREQUENCY_in Leukocytes"] = "NA"
	gate_frame_PBMC.population["CD15posCD14low_LDGs_FREQUENCY_in PBMC"] = "NA"	
	gate_frame_PBMC.parameters = ["CD15 PE-A","CD14 PC7-A"]
	bag_of_frame.append(gate_frame_PBMC)

	## ALIVE gate frame.
	gate_frame_alive = gate_frame()
	gate_frame_alive.name = "ALIVE"
	gate_frame_alive.root = gate_frame_S4
	gate_frame_alive.population["Monocytes_CONCENTRATION_"] = "NA"
	gate_frame_alive.parameters = ["CD4 PB-A","SSC-A"]
	bag_of_frame.append(gate_frame_alive)

	## MONO gate frame.
	gate_frame_mono = gate_frame()
	gate_frame_mono.name = "MONO"
	gate_frame_mono.root = gate_frame_alive
	# -> concentration
	gate_frame_mono.population["CD14pos_monocytes_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_mono.population["CD14pos_monocytes_FREQUENCY_in Monocytes"] = "NA"
	gate_frame_mono.parameters = ["CD14"]
	bag_of_frame.append(gate_frame_mono)

	## MONO gate frame.
	gate_frame_monobis = gate_frame()
	gate_frame_monobis.name = "MONObis"
	gate_frame_monobis.root = gate_frame_mono
	gate_frame_monobis.population["CD14lowCD16pos_nonclassicalMonocytes_CONCENTRATION_"] = "NA"
	gate_frame_monobis.population["CD14posCD16pos_intermediateMonocytes_CONCENTRATION_"] = "NA"
	gate_frame_monobis.population["CD14highCD16neg_classicalMonocytes_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_monobis.population["CD14lowCD16pos_nonclassicalMonocytes_FREQUENCY_in CD14pos_monocytes"] = "NA"
	gate_frame_monobis.population["CD14posCD16pos_intermediateMonocytes_FREQUENCY_in CD14pos_monocytes"] = "NA"
	gate_frame_monobis.population["CD14highCD16neg_classicalMonocytes_FREQUENCY_in CD14pos_monocytes"] = "NA"
	gate_frame_monobis.parameters = ["CD14 PC7-A", "CD15 PE-A"]
	bag_of_frame.append(gate_frame_monobis)

	

	## LY gate frame.
	gate_frame_ly = gate_frame()
	gate_frame_ly.name = "LY"
	gate_frame_ly.root = gate_frame_S4
	# -> concentration
	gate_frame_ly.population["CD19pos_Bcells_CONCENTRATION_"] = "NA"
	gate_frame_ly.population["CD3pos_Tcells_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_ly.population["CD3pos_Tcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_ly.population["CD19pos_Bcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_ly.population["CD19pos_Bcells_FREQUENCY_in Leukocytes"] = "NA"
	gate_frame_ly.population["CD19pos_Bcells_FREQUENCY_in PBMC"] = "NA"
	gate_frame_ly.parameters = ["CD19 APC-A", "CD3 APC-AF750-A"]
	bag_of_frame.append(gate_frame_ly)




	## T CELLS and NOT CD3+CD56+
	gate_frame_TCELLS_and_NOT_CD3CD56 = gate_frame()
	gate_frame_TCELLS_and_NOT_CD3CD56.name = "T CELLS and NOT CD3+CD56+"
	gate_frame_TCELLS_and_NOT_CD3CD56.root = gate_frame_ly
	# -> concentration
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD4-CD8+"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8neg_CD4neg_Tcells_CONCENTRATION_"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8pos_CD4pos_Tcells_CONCENTRATION_"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD4+CD8-"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD4pos_Tcells_CONCENTRATION_"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8pos_Tcells_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8pos_Tcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8pos_Tcells_FREQUENCY_in CD3pos_Tcells"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8pos_CD4pos_Tcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8pos_CD4pos_Tcells_FREQUENCY_in CD3pos_Tcells"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8neg_CD4neg_Tcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD8neg_CD4neg_Tcells_FREQUENCY_in CD3pos_Tcells"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD4pos_Tcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.population["CD4pos_Tcells_FREQUENCY_in CD3pos_Tcells"] = "NA"
	gate_frame_TCELLS_and_NOT_CD3CD56.parameters = ["CD8 KO-A", "CD4 PB-A"]
	bag_of_frame.append(gate_frame_TCELLS_and_NOT_CD3CD56)

	## LYbis gate frame.
	gate_frame_lybis = gate_frame()
	gate_frame_lybis.name = "LYbis"
	gate_frame_lybis.root = gate_frame_S4
	# -> concentration
	gate_frame_lybis.population["CD3posCD56pos_NklikeTcells_CONCENTRATION_"] = "NA"
	gate_frame_lybis.population["CD3negCD56pos_NKcells_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_lybis.population["CD3posCD56pos_NklikeTcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_lybis.population["CD3negCD56pos_NKcells_FREQUENCY_in Lymphocytes"] = "NA"
	gate_frame_lybis.population["CD3negCD56pos_NKcells_FREQUENCY_in Leukocytes"] = "NA"
	gate_frame_lybis.population["CD3negCD56pos_NKcells_FREQUENCY_in PBMC"] = "NA"
	gate_frame_lybis.population["CD3posCD56pos_NklikeTcells_FREQUENCY_in CD3pos_Tcells"] = "NA"
	gate_frame_lybis.parameters = ["CD3 APC-AF750-A", "CD56 PC5-5-A"]
	bag_of_frame.append(gate_frame_lybis)

	## NK CELLS gate frame.
	gate_frame_nkcells = gate_frame()
	gate_frame_nkcells.name = "NK CELLS"
	gate_frame_nkcells.root = gate_frame_lybis
	# -> concentration
	gate_frame_nkcells.population["CD56high_CD16low_CONCENTRATION_"] = "NA"
	gate_frame_nkcells.population["CD56low_CD16high_CONCENTRATION_"] = "NA"
	# -> frequencies
	gate_frame_nkcells.population["CD56high_CD16low_FREQUENCY_in CD3negCD56pos_NKcells"] = "NA"
	gate_frame_nkcells.population["CD56low_CD16high_FREQUENCY_in CD3negCD56pos_NKcells"] = "NA"

	gate_frame_nkcells.parameters = ["CD16 FITC-A", "CD56 PC5-5-A"]
	bag_of_frame.append(gate_frame_nkcells)
	

	## return the list of gate frame
	return bag_of_frame



def populate_panel_1(data_file):
	"""
	IN PROGRESS
	"""

	## importation
	import pandas as pd

	## parameters
	patient_id_to_panel = {}

	dataset = pd.read_csv(data_file, sep=";")

	for index, row in dataset.iterrows():

		patient_id = row['patient ID']
		panel_1 = create_panel_1_structure()

		for gate_frame in panel_1:
			for pop_name in row.keys():
				if(pop_name in gate_frame.population.keys()):
					gate_frame.population[pop_name] = row[pop_name]
		
		patient_id_to_panel[patient_id] = panel_1

	return patient_id_to_panel


def map_the_way_to_target(origin, target, panel_structure):
	"""
	"""

	origin_to_target = []
	start_node = "NA"
	destination_reach = False

	## catch the origin pop
	for gate_frame in panel_structure:
		for pop_name in gate_frame.population.keys():
			if(pop_name == origin):
				origin_to_target.append(gate_frame.name)
				start_node = gate_frame
	
	while(not destination_reach):
		
		if(start_node.root == None):
			break

		transitory_node = start_node.root
		for pop_name in transitory_node.population.keys():
			if(pop_name == target):
				origin_to_target.append(transitory_node.name)
				destination_reach = True

		if(not destination_reach):
			origin_to_target.append(transitory_node.name)


		start_node = transitory_node

	print(origin_to_target)







## TEST SPACE ##

gate1 = gate_frame()
gate1.name = "FirstGate"
gate1.population["BigPop1_total"] = 100.0
gate1.population["SmallPop1_freq"] = 1.0

gate2 = gate_frame()
gate2.name = "SecondGate"
gate2.population["SmallPop1_total"] = 50
gate2.population["SmallPop1_freq"] = 0.5
gate2.root = gate1

gate3 = gate_frame()
gate3.name = "ThirdGate"
gate3.population["SmallPop1_total"] = 25
gate3.population["SmallPop1_freq"] = 0.5
gate3.root = gate2

gate4 = gate_frame()
gate4.name = "FourthGate"
gate4.population["SmallPop1_total"] = 15
gate4.population["SmallPop1_freq"] = 0.5
gate4.root = gate2


tree_structure = [gate1, gate2, gate3, gate4]

compute_back_frequency(gate3, "SmallPop1_freq")

frame_to_child = trace_tree(tree_structure)

p1 = create_panel_1_structure()
frame_to_child = trace_tree(p1)



stuff = populate_panel_1("/home/nurtal/Spellcraft/Bdata/Panel_1_concat_transformed.csv")


## map test
"""
target = "Monocytes_CONCENTRATION_"
origin = "CD14lowCD16pos_nonclassicalMonocytes_CONCENTRATION_"
structure = frame_to_child
map_the_way_to_target(origin, target, p1)
"""

pop_name = "CD3posCD56pos_NklikeTcells_FREQUENCY_in CD3pos_Tcells"
pop_number = 17
stuff = get_pop_name(pop_number)

stuff = get_gate_name(pop_number)

stuff = create_population_structure(21)

stuff = create_panel_1_populations()


get_frequencies(29, 9, stuff)