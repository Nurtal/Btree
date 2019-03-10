







def select_candidate(var_list, target):
	"""
	"""

	## parameters
	selected_var = None

	## check if the answer is in the question
	for var in var_list:
		var_in_array = var.split("_FREQUENCY_in ")
		if(var_in_array[1] == target):
			selected_var = var
			break

	## check if ...
	if(selected_var != None):



	print(selected_var)





def compute_frquencies(patient_id, origin, target):
	"""
	"""

	## importation
	import pandas as pd

	## parameters
	dataset_file = "/home/nurtal/Spellcraft/Bdata/Panel_1_concat_transformed.csv"
	selected_row = None
	origin_var = None
	reach_target = False
	values_to_target = []
	trace = []
	var_candidates = []

	dataset = pd.read_csv(dataset_file, sep=";")

	for index, row in dataset.iterrows():
		if(patient_id == row['patient ID']):
			selected_row = row

	## Find the stat already computed
	for var_name in selected_row.keys():
		var_name_in_array = var_name.split("_FREQUENCY_in ")
		if(len(var_name_in_array) > 1):
			if(var_name_in_array[0] == origin and var_name_in_array[1] == target):
				values_to_target.append(selected_row[var_name])
				trace.append(var_name)
				reach_target = True
				break

	## compute inexisting frequencies
	while(not reach_target):

		## loop over dataset
		for var_name in selected_row.keys():
			var_name_in_array = var_name.split("_FREQUENCY_in ")

			## select freqeuncy dataset with the first part
			## match to origin
			if(len(var_name_in_array) > 1):
				if(var_name_in_array[0] == origin):
					print(var_name_in_array[0])
					var_candidates.append(var_name)

		## evaluate number of variable candidates
		if(len(var_candidates) > 1):
			for var in var_candidates:

				print(var_candidates)

				## TODO : pick one variable from the
				## list of candidates and process
				values_to_target.append(selected_row[var])
				trace.append(var)
				var_name_in_array = var.split("_FREQUENCY_in ")
				origin = var_name_in_array[1]
				var_candidates = []
		else:

			## pick the only candidate
			var = var_candidates[0]
				
			## process data
			values_to_target.append(selected_row[var])
			trace.append(var)

			## update origin pop
			var_name_in_array = var.split("_FREQUENCY_in ")
			origin = var_name_in_array[1]
				
			## re-init candidates list
			var_candidates = []

			## update reach targer status
			if(origin == target):
				reach_target = True

	




	







	print(values_to_target)
	print(trace)





var_candidates = ['CD3negCD56pos_NKcells_FREQUENCY_in Lymphocytes', 'CD3negCD56pos_NKcells_FREQUENCY_in Leukocytes', 'CD3negCD56pos_NKcells_FREQUENCY_in PBMC']
select_candidate(var_candidates, "Lymphocytes")

"""
origin = "CD56high_CD16low"
#origin = "CD19pos_Bcells"
target = "Lymphocytes"
compute_frquencies(32150687, origin, target)
"""


