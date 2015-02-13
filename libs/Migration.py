import numpy as np
import scipy as sp

def migration_simple(integrated_overload_index,relocation_thresholds, placement_matrix, load_physical):

   # initialization
	migrate = 0;
	migration_selected = 0;
	migration_source = 0;
	migration_destination = 0;

	migrate_me_maybe = integrated_overload_index > relocation_thresholds;
	if np.sum(migrate_me_maybe) > 0
		migrate = 1;
		indexes = find(migrate_me_maybe == 1);
		# random migration order among overloaded physical machines
		migration_source = randperm(length(indexes));
		migration_source = indexes(migration_source); # select one migration source
		migration_source = migration_source(1, 1);
		# random the choice of virtual machines among the one of source
		vm_set_migration = find(placement_matrix(:, migration_source) == 1);
		migration_options = randperm(length(vm_set_migration));
		migration_selected = vm_set_migration(migration_options(1,1)); # migrate me
		# select destionation
		[val, migration_destination] = min(load_physical);     
		fprintf('[SIMPLE] Asked to migrate %d from %d to %d\n',\
			migration_selected, migration_source, migration_destination);

	return migrate, migration_selected, migration_source,migration_destination

