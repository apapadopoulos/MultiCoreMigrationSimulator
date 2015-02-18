clear; close all; clc;

%% Load data
simple          = load('simple_data.mat');
load_aware      = load('load_aware_data.mat');
load_normalized = load('load_normalized_data.mat');

numExperiments = length(simple.data);
numCores   = zeros(numExperiments,1);
numThreads = zeros(numExperiments,1);
threshold  = zeros(numExperiments,1);
for i=1:numExperiments
    numCores(i)   = simple.data(i).numCores;
    numThreads(i) = simple.data(i).numThreads;
    threshold(i)  = simple.data(i).relocationThreshold;
end

nC = unique(numCores);
nT = unique(numThreads);
th = unique(threshold);

simple_migrations = zeros(length(nC),length(nT),length(th));
load_aware_migrations = zeros(length(nC),length(nT),length(th));
load_normalized_migrations = zeros(length(nC),length(nT),length(th));
for i=1:numExperiments
    simple_migrations(nC==simple.data(i).numCores,...
                      nT==simple.data(i).numThreads,...
                      th==simple.data(i).relocationThreshold)...
                      = simple.data(i).totMig(end);
                  
    load_aware_migrations(nC==load_aware.data(i).numCores,...
                          nT==load_aware.data(i).numThreads,...
                          th==load_aware.data(i).relocationThreshold)...
                          = load_aware.data(i).totMig(end);
    load_normalized_migrations(nC==load_normalized.data(i).numCores,...
                               nT==load_normalized.data(i).numThreads,...
                               th==load_normalized.data(i).relocationThreshold)...
                               = load_normalized.data(i).totMig(end);
    
end

%% Plotting results
colormap jet
cm = colormap;

[nCores,Thresh] = meshgrid(nC,th);
figure(1); hold on;
for i=1:length(nT)
    hSurface = surf(nCores,Thresh,...
        reshape(simple_migrations(:,i,:),[length(nC),length(th)])');
    set(hSurface,'FaceColor',cm(10*i,:),'FaceAlpha',0.5);
end
hold off;
title('Simple');
xlabel('cores');
ylabel('thresholds');
zlabel('migrations')
view(3);

figure(2); hold on;
for i=1:length(nT)
    hSurface = surf(nCores,Thresh,...
        reshape(load_aware_migrations(:,i,:),[length(nC),length(th)])');
    set(hSurface,'FaceColor',cm(10*i,:),'FaceAlpha',0.5);
end
hold off;
title('Load aware');
xlabel('cores');
ylabel('thresholds');
zlabel('migrations')
view(3);

figure(3); hold on;
for i=1:length(nT)
    hSurface = surf(nCores,Thresh,...
        reshape(load_normalized_migrations(:,i,:),[length(nC),length(th)])');
    set(hSurface,'FaceColor',cm(10*i,:),'FaceAlpha',0.5);
end
hold off;
title('Load normalized');
xlabel('cores');
ylabel('thresholds');
zlabel('migrations')
view(3);
