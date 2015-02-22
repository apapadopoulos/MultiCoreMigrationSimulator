clear; close all; clc;

%% Load data
simple          = load('simple_data.mat');
load_aware      = load('load_aware_data.mat');
load_normalized = load('load_normalized_data.mat');

numExperiments = length(simple.data);
numCores   = zeros(numExperiments,1);
numThreads = zeros(numExperiments,1);
for i=1:numExperiments
    numCores(i)   = simple.data(i).numCores;
    numThreads(i) = simple.data(i).numThreads;
end

nC = unique(numCores);
nT = unique(numThreads);

simple_migrations = zeros(length(nC),length(nT));
load_aware_migrations = zeros(length(nC),length(nT));
load_normalized_migrations = zeros(length(nC),length(nT));
for i=1:numExperiments
    simple_migrations(nC==simple.data(i).numCores,...
                      nT==simple.data(i).numThreads)...
                      = simple.data(i).totMig(end);
                  
    load_aware_migrations(nC==load_aware.data(i).numCores,...
                          nT==load_aware.data(i).numThreads)...
                          = load_aware.data(i).totMig(end);
    load_normalized_migrations(nC==load_normalized.data(i).numCores,...
                               nT==load_normalized.data(i).numThreads)...
                               = load_normalized.data(i).totMig(end);
    
end

%% Plotting results
colormap jet
cm = colormap;

[nCores,nThreads] = meshgrid(nC,nT);
figure(1); hold on;
hSurface = surf(nCores,nThreads,simple_migrations);
set(hSurface,'FaceColor',cm(1,:),'FaceAlpha',0.5);
hold off;
title('Simple');
xlabel('cores');
ylabel('threads');
zlabel('migrations')
view(3);

figure(2); hold on;
hSurface = surf(nCores,nThreads,load_aware_migrations);
set(hSurface,'FaceColor',cm(10,:),'FaceAlpha',0.5);
hold off;
title('Load_aware');
xlabel('cores');
ylabel('threads');
zlabel('migrations')
view(3);


figure(3); hold on;
hSurface = surf(nCores,nThreads,load_normalized_migrations);
set(hSurface,'FaceColor',cm(20,:),'FaceAlpha',0.5);
hold off;
title('Load normalized');
xlabel('cores');
ylabel('threads');
zlabel('migrations')
view(3);

%% Comparative analysis
figure(4); hold on;
hSurface = surf(nCores,nThreads,simple_migrations);
set(hSurface,'FaceColor',cm(1,:),'FaceAlpha',0.5);
hSurface = surf(nCores,nThreads,load_aware_migrations);
set(hSurface,'FaceColor',cm(end/2,:),'FaceAlpha',0.5);
hSurface = surf(nCores,nThreads,load_normalized_migrations);
set(hSurface,'FaceColor',cm(end,:),'FaceAlpha',0.5);
hold off;
title('Load normalized');
xlabel('cores');
ylabel('threads');
zlabel('migrations')
view(3);
