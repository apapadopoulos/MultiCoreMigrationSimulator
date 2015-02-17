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
        numCores   = str2num(nums{1});
        numThreads = str2num(nums{2});
        relocationThreshold = str2num([nums{3} '.' nums{4}]);
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

% Loading the results
clearvars -except res_dir names;
simple          = load('simple_data.mat');
load_aware      = load('load_aware_data.mat');
load_normalized = load('load_normalized_data.mat');

%% Analyzing the number of migrations
numExperiments = length(simple.data);

simple_migrations          = zeros(numExperiments,1);
load_aware_migrations      = zeros(numExperiments,1);
load_normalized_migrations = zeros(numExperiments,1);

for i=1:numExperiments
    temp = simple.data(i).totMig;
    simple_migrations(i)          = temp(end);
    temp = load_aware.data(i).totMig;
    load_aware_migrations(i)      = temp(end);
    temp = load_normalized.data(i).totMig;
    load_normalized_migrations(i) = temp(end);
end

simple_avg_migrations          = mean(simple_migrations);
load_aware_avg_migrations      = mean(load_aware_migrations);
load_normalized_avg_migrations = mean(load_normalized_migrations);

%% Show an example of execution
exper = 35;
% Simple
figure(1); clf;
subplot(311);
hold on;
  plot(simple.data(exper).time,simple.data(exper).U);
  plot(simple.data(exper).time,simple.data(exper).sp,'k--');
  ylim([0,1]);
hold off;
subplot(312);
hold on;
  plot(simple.data(exper).time,simple.data(exper).Un);
  plot(simple.data(exper).time,simple.data(exper).sp,'k--');
  ylim([0,10]);
hold off;
subplot(313);
hold on;
  plot(simple.data(exper).time,simple.data(exper).OI);
  plot(simple.data(exper).time,...
      simple.data(exper).relocationThreshold*ones(length(simple.data(exper).time),1),'k--');
  ylim([0,1]);
hold off;

% Load_aware
figure(2); clf;
subplot(311);
hold on;
  plot(load_aware.data(exper).time,load_aware.data(exper).U);
  plot(load_aware.data(exper).time,load_aware.data(exper).sp,'k--');
  ylim([0,1]);
hold off;
subplot(312);
hold on;
  plot(load_aware.data(exper).time,load_aware.data(exper).Un);
  plot(load_aware.data(exper).time,load_aware.data(exper).sp,'k--');
  ylim([0,10]);
hold off;
subplot(313);
hold on;
  plot(load_aware.data(exper).time,load_aware.data(exper).OI);
  plot(load_aware.data(exper).time,...
      load_aware.data(exper).relocationThreshold*ones(length(load_aware.data(exper).time),1),'k--');
  ylim([0,1]);
hold off;

% Load_aware
figure(3); clf;
subplot(311);
hold on;
  plot(load_normalized.data(exper).time,load_normalized.data(exper).U);
  plot(load_normalized.data(exper).time,load_normalized.data(exper).sp,'k--');
  ylim([0,1]);
hold off;
subplot(312);
hold on;
  plot(load_normalized.data(exper).time,load_normalized.data(exper).Un);
  plot(load_normalized.data(exper).time,load_normalized.data(exper).sp,'k--');
  ylim([0,10]);
hold off;
subplot(313);
hold on;
  plot(load_normalized.data(exper).time,load_normalized.data(exper).OI);
  plot(load_normalized.data(exper).time,...
      load_normalized.data(exper).relocationThreshold*ones(length(load_normalized.data(exper).time),1),'k--');
hold off;
ylim([0,1]);