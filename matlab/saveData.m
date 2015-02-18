clear;
clc;

%% Load data
res_dir = '../results/';

fprintf('Loading files:\n');
names = {'load_aware' 'load_normalized' 'simple'};
folders = cell(length(names),1);
for i=1:length(names)
    folders{i} = [res_dir names{i} '/'];
end
delimiterIn = ',';
headerlinesIn = 1;

for i=1:length(folders)
    files_struct = dir([folders{i} '*.csv']);
    files = {files_struct.name};
    clear data
    for j = 1:length(files)
        nums = regexp(files{j},'\d+','match');
        numCores   = str2double(nums{1});
        numThreads = str2double(nums{2});
        padding = str2double([nums{3} '.' nums{4}]);
        relocationThreshold = str2double([nums{4} '.' nums{5}]);
        clear D
        fprintf('%d/%d: %s%s\n',j,length(files),folders{i},files{j});
        D = importdata([folders{i} files{j}],delimiterIn,headerlinesIn);
        data(j).id     = files{j}(1:end-4);
        data(j).time   = D.data(:,1);
        data(j).sp     = D.data(:,2+0*numCores:2+1*numCores-1);
        data(j).Un     = D.data(:,2+1*numCores:2+2*numCores-1);
        data(j).U      = D.data(:,2+2*numCores:2+3*numCores-1);
        data(j).OI     = D.data(:,2+3*numCores:2+4*numCores-1);
        data(j).totMig = D.data(:,end);
        
        data(j).numCores   = numCores;
        data(j).numThreads = numThreads;
        data(j).relocationThreshold = relocationThreshold;
    end
    save([names{i} '_data.mat'],'data','-v7.3');
end