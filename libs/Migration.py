import numpy as np
import scipy as sp
import random

class MigrationManager:
	""" Migration manager decides when to migrate a process from one core to another.
		It implements different migration policies:
		- migration_simple -> in case of overload in one core, it migrate to a random core
	"""
	def __init__(self,numCores,relocation_thresholds):
		self.numCores = numCores
		self.integrated_overload_index = np.zeros(self.numCores)
		self.relocation_thresholds = relocation_thresholds
		self.total_migrations = 0  # counter for the number of migrations

	def migration_simple(self,schedulerList, placement_matrix):

	   # initialization
		migrate = 0;
		migration_selected = -1
		migration_source = -1
		migration_destination = -1

		self.integrated_overload_index += np.array([schedulerList[i].getUtilization() for i in xrange(0,self.numCores)])


		migrate_me_maybe = self.integrated_overload_index > self.relocation_thresholds
		if np.any(migrate_me_maybe) == True:
			migrate = 1
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
				placement_matrix[migration_selected,migration_source]      = 0
				placement_matrix[migration_selected,migration_destination] = 1

				self.total_migrations += 1

				# resetting the integrated index
				self.integrated_overload_index[migration_source] = 0
				print '[SIMPLE] Asked to migrate process at index %d from Core%d to Core%d'%\
				                (migration_selected,migration_source,migration_destination)
			else:
				# no cores are underloaded
				#print '[SIMPLE] No migration possible'
				migration_destination = migration_source

		return placement_matrix


	def getTotalMigration(self):
		return self.total_migrations

