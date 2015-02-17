import numpy as np
import scipy as sp
import random

## TODOs:
#  - re-write all the for loops in a more efficient way
#  - better exploit inheritance
#  - add migration of multiple process

class MigrationManager:
	""" Migration manager decides when to migrate a process from one core to another.
		It implements different migration policies:
		- migration_simple -> in case of overload in one core, it migrate to a random core
	"""
	def __init__(self, numCores, relocation_thresholds, padding=1.1, minLoad=0.0, maxLoad=1.0):
		self.numCores = numCores
		self.integrated_overload_index = np.zeros(self.numCores)
		self.relocation_thresholds = relocation_thresholds
		self.total_migrations = 0  # counter for the number of migrations
		self.padding = padding
		self.minLoad = minLoad
		self.maxLoad = maxLoad

	def migrate(self, placement_matrix, thread,source,dest):
		# update the placement_matrix
		placement_matrix[thread,source] = 0
		placement_matrix[thread,dest]   = 1
		# increase the number of migrations
		self.total_migrations += 1
		# resetting the integrated index
		self.integrated_overload_index[source] = 0

		return placement_matrix

	def normalize_load(self, schedulerList):
		## Normalize the load with respect to the actual utilization
		utilization = np.array([schedulerList[i].getUtilization()\
			                      for i in xrange(0,self.numCores)])
		avg_utilization = max(min(np.sum(utilization)/self.numCores,self.maxLoad),self.minLoad)
		utilization_set_point = self.padding*avg_utilization*np.ones(self.numCores)
		return utilization_set_point

	def updatedOverloadIndex(self, schedulerList, utilization_set_point):
		## Update the value of the integrated overload index
		utilization = np.array([schedulerList[i].getUtilization()\
			                      for i in xrange(0,self.numCores)])
		tauros      = np.array([schedulerList[i].getTauro()\
			                      for i in xrange(0,self.numCores)])
		delta = np.zeros(self.numCores)
		for i in xrange(0,self.numCores):
			if utilization[i] > 0: # If the core is in use
				delta[i] = (utilization[i] - utilization_set_point[i])/utilization[i]*tauros[i]
			else: # If the core is not in use
				delta[i] = 0
		increment   = np.array([max(delta[i],0) for i in xrange(0,self.numCores)])
		self.integrated_overload_index += increment

	def argMaxSet(self, vec):
		# Find all the indices with maximum value
		max_val = np.max(vec)
		indices = [i for i in xrange(0,len(vec)) if vec[i]==max_val]
		return indices

	def argMinSet(self, vec):
		# Find all the indices with minimum value
		min_val = np.min(vec)
		indices = [i for i in xrange(0,len(vec)) if vec[i]==min_val]
		return indices

	def argMaxRand(self, vec):
		# Find the index with maximum value. If there is more than one
		# a random index is chosen
		indices = self.argMaxSet(vec)
		index = random.choice(indices)
		return index

	def getTotalMigrations(self):
		return self.total_migrations

	def getOverloadIndex(self):
		return self.integrated_overload_index

	def viewTotalMigrations(self):
		print 'Total migrations = %d'%self.getTotalMigrations()

	########################
	# Migration algorithms 
	########################
	def migration_simple(self, schedulerList, placement_matrix, utilization_set_point):

	   # initialization
		migration_selected = -1
		migration_source = -1
		migration_destination = -1

		# update the integrated overload index for all the cores
		self.updatedOverloadIndex(schedulerList,utilization_set_point)

		migrate_me_maybe = self.integrated_overload_index > self.relocation_thresholds
		if np.any(migrate_me_maybe) == True:
			indexes_true  = [i for i in xrange(0,self.numCores) if migrate_me_maybe[i] == True]
			indexes_false = [i for i in xrange(0,self.numCores) if migrate_me_maybe[i] == False]

			# migrate a ramdom core from which to choose a thread to migrate
			migration_source = random.choice(indexes_true)
			if len(indexes_false) > 0:
				# random the choice of the destination core
				index_threads = [i for i in xrange(0,len(placement_matrix[:,migration_source]))\
				                         if placement_matrix[i,migration_source]==1]
				# choosing a random thread to migrate
				migration_selected = random.choice(index_threads)
				migration_destination = random.choice(indexes_false)

				# migrating the process on the placement_matrix
				placement_matrix = self.migrate(placement_matrix,\
					                            migration_selected,\
					                            migration_source,\
					                            migration_destination)
				print '[SIMPLE] Asked to migrate process at index %d from Core%d to Core%d'%\
				                (migration_selected,migration_source,migration_destination)
			else:
				# no cores are underloaded
				#print '[SIMPLE] No migration possible'
				migration_destination = migration_source

		return placement_matrix		

	def migration_load_aware(self, schedulerList, placement_matrix, utilization_set_point, alphas):

		# initialization
		migration_selected = -1
		migration_source = -1
		migration_destination = -1

		# update the integrated overload index for all the cores
		self.updatedOverloadIndex(schedulerList,utilization_set_point)

		migrate_me_maybe = self.integrated_overload_index > self.relocation_thresholds
		if np.any(migrate_me_maybe) == True: # If there is any overloaded core
			# find the indices of overloaded cores
			indexes_true  = [i for i in xrange(0,self.numCores) if migrate_me_maybe[i] == True]
			# find the indices of not overloaded cores
			indexes_false = [i for i in xrange(0,self.numCores) if migrate_me_maybe[i] == False]

			# migrate the core with a larger value of the overload index
			# if there are more than one with the same overload index, pick one at random
			migration_source = self.argMaxRand(self.integrated_overload_index)

			if len(indexes_false) > 0: # if there are any underloaded cores
				# finding the threads running on the migration_source core
				numTotThreads = len(placement_matrix[:,migration_source])
				index_threads = [i for i in xrange(0,numTotThreads)\
				                         if placement_matrix[i,migration_source]==1]
				
				# computing the spare capacity the underloaded cores
				spare_capacity = [utilization_set_point[i]-schedulerList[i].getUtilization()\
				                                   for i in indexes_false]

				# constructing the matrix of all the possible migrations
				possible_couples    = [(i,alphas[i],j) for i in index_threads for j in indexes_false]
				possible_migrations = [abs(j - alphas[i]) for i in index_threads\
				                                          for j in spare_capacity]

				# Identifying which is the best migration
				indices_possible_migrations = self.argMinSet(possible_migrations)
				alphas_migration_list = [possible_couples[i][1] for i in indices_possible_migrations]
				idx_migration = self.argMaxRand(alphas_migration_list)

				#print idx_migration
				migration_selected,temp,migration_destination = possible_couples[idx_migration]

				# migrating the process on the placement_matrix
				placement_matrix = self.migrate(placement_matrix,\
					                            migration_selected,\
					                            migration_source,\
					                            migration_destination)
				print '[LOAD_AWARE] Asked to migrate process at index %d from Core%d to Core%d'%\
				                (migration_selected,migration_source,migration_destination)
			else:
				# no cores are underloaded
				#print '[SIMPLE] No migration possible'
				migration_destination = migration_source

		return placement_matrix

