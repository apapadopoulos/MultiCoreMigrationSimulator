clear;
clc;

%% Load data
simple          = load('simple_data.mat');
load_aware      = load('load_aware_data.mat');
load_normalized = load('load_normalized_data.mat');

%% Analyzing the number of migrations
numExperiments = length(simple.data);
timeHorizon    = length(simple.data(1).time);

simple_migrations          = zeros(numExperiments,1);
load_aware_migrations      = zeros(numExperiments,1);
load_normalized_migrations = zeros(numExperiments,1);

simple_fairness = zeros(numExperiments,timeHorizon);
simple_fairness_nom = zeros(numExperiments,timeHorizon);

load_aware_fairness = zeros(numExperiments,timeHorizon);
load_aware_fairness_nom = zeros(numExperiments,timeHorizon);

load_normalized_fairness = zeros(numExperiments,timeHorizon);
load_normalized_fairness_nom = zeros(numExperiments,timeHorizon);

for i=1:numExperiments
    temp = simple.data(i).totMig;
    simple_migrations(i)          = temp(end);
    temp = load_aware.data(i).totMig;
    load_aware_migrations(i)      = temp(end);
    temp = load_normalized.data(i).totMig;
    load_normalized_migrations(i) = temp(end);
    for kk=1:timeHorizon
        simple_fairness(i,kk) = jainIndex(simple.data(i).U(kk,:));
        simple_fairness_nom(i,kk) = jainIndex(simple.data(i).Un(kk,:));
        
        load_aware_fairness(i,kk) = jainIndex(load_aware.data(i).U(kk,:));
        load_aware_fairness_nom(i,kk) = jainIndex(load_aware.data(i).Un(kk,:));
        
        load_normalized_fairness(i,kk) = jainIndex(load_normalized.data(i).U(kk,:));
        load_normalized_fairness_nom(i,kk) = jainIndex(load_normalized.data(i).Un(kk,:));
    end
end

simple_avg_migrations          = mean(simple_migrations);
load_aware_avg_migrations      = mean(load_aware_migrations);
load_normalized_avg_migrations = mean(load_normalized_migrations);




%% Show an example of execution
exper = 2;
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

subplot(311);
title('Simple');

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

subplot(311);
title('Load aware');

% Load_normalized
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

subplot(311);
title('Load normalized');

figure(4); clf;
subplot(311);
hold on;
plot(simple.data(exper).time,simple_fairness(exper,:),'b');
plot(simple.data(exper).time,simple_fairness_nom(exper,:),'k');
hold off;

subplot(312);
hold on;
plot(simple.data(exper).time,load_aware_fairness(exper,:),'b');
plot(simple.data(exper).time,load_aware_fairness_nom(exper,:),'k');
hold off;

subplot(313);
hold on;
plot(simple.data(exper).time,load_normalized_fairness(exper,:),'b');
plot(simple.data(exper).time,load_normalized_fairness_nom(exper,:),'k');
hold off;
