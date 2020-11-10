
load('TrainingSamplesDCT_8.mat')

fg_indexs = zeros(1, size(TrainsampleDCT_FG, 1)); % P(x|cheetah)
bg_indexs =  zeros(1, size(TrainsampleDCT_BG, 1)); % P(x|grass)


n_grass = size(TrainsampleDCT_BG, 1);
n_cheetah = size(TrainsampleDCT_FG, 1);
pi_vals = 0:.001:2;
def_var = 1;
grass_pi_res = zeros(64,1);
cheetah_pi_res= zeros(64,1);
grass_var_res = zeros(64,1);
cheetah_var_res= zeros(64,1);

figure(1)
for i = 1:64
    grass_vals = zeros(length(TrainsampleDCT_FG), 1);

    for j=1:length(TrainsampleDCT_FG)
        grass_vals(j) = TrainsampleDCT_FG(j, i);
    end
    cheetah_vals = zeros(length(TrainsampleDCT_BG), 1);
    for j=1:length(TrainsampleDCT_BG)
        cheetah_vals(j) = TrainsampleDCT_BG(j, i);
    end
    
    n_grass =  length(grass_vals);
    n_cheetah = length(cheetah_vals);
    
    grass_res = zeros(n_grass, 1);
    cheetah_res = zeros(n_cheetah, 1);
    
    for j=1:length(pi_vals)
        grass_res(j) = exp(-.5 * sum((grass_vals - pi_vals(j)).^2)/def_var);
    end
    for j=1:length(pi_vals)
        cheetah_res(j) = exp(-.5 * sum((cheetah_vals - pi_vals(j)).^2)/def_var);
    end
    [gm, gi] = max(grass_res);
    [cm, ci] = max(cheetah_res);
    
    grass_pi = pi_vals(gi);
    cheetah_pi = pi_vals(ci);

    grass_var = sum((grass_vals - grass_pi).^2) / (n_grass);
    cheetah_var = sum((cheetah_vals - cheetah_pi).^2) / (n_cheetah);
    
    % This is just for clarity, otherwise charts are empty
    if isnan(grass_var) || grass_var == 0
        grass_var = 1;
    end
    if isnan(cheetah_var) || cheetah_var ==0
        cheetah_var = 1;
    end
    
    grass_pi_res(i) = grass_pi;
    grass_var_res(i) = grass_var;
    cheetah_pi_res(i) = cheetah_pi;
    cheetah_var_res(i) = cheetah_var;
    
    
    allvals = cat(1, grass_vals, cheetah_vals);
    x_vals = min(allvals):.0001:max(allvals);
    grass_dist = gaussianPDF(x_vals, grass_pi, sqrt(grass_var));
    cheetah_dist = gaussianPDF(x_vals, cheetah_pi, sqrt(cheetah_var));

    subplot(8,8,i)
    l1 = plot(x_vals, grass_dist, "Color", "g");
    hold on
    l2 = plot(x_vals, cheetah_dist, "Color", "r", "LineStyle", "--");
    hold on
    title(sprintf("Index: %d", i));
end
hold off
hl = legend([l1,l2], {"Grass", "Cheetah"});
set(hl, "Position", [.1, .1, .2, .2]);
sgtitle("Gaussian Dist of each index");


% Best 8 (Visual)
disp("Best 8 Based on visual")
disp("Index: 1, 12, 15, 17, 23, 24, 25, 32")
disp("These are the best features because we can see the distributions for each feature given grass or cheetah are very different. That is the distirbution overlaps the least. Additionally, low variance is ideal because it means the distribution is more certain.")
figure(2)
features = [1, 12, 15,17,23,24,25, 32];
for idx=1:length(features)
    i = features(idx);
    % Getting values again 
        grass_vals = zeros(length(TrainsampleDCT_FG), 1);

    for j=1:length(TrainsampleDCT_FG)
        grass_vals(j) = TrainsampleDCT_FG(j, i);
    end
    cheetah_vals = zeros(length(TrainsampleDCT_BG), 1);
    for j=1:length(TrainsampleDCT_BG)
        cheetah_vals(j) = TrainsampleDCT_BG(j, i);
    end
    % Plottings
    grass_pi = grass_pi_res(i);
    grass_var = grass_var_res(i);
    cheetah_pi = cheetah_pi_res(i);
    cheetah_var = cheetah_var_res(i);
    
    allvals = cat(1, grass_vals, cheetah_vals);
    x_vals = min(allvals):.0001:max(allvals);
    grass_dist = gaussianPDF(x_vals, grass_pi, sqrt(grass_var));
    cheetah_dist = gaussianPDF(x_vals, cheetah_pi, sqrt(cheetah_var));
    subplot(2,4,idx)
    l1 = plot(x_vals, grass_dist, "Color", "g");
    hold on
    l2 = plot(x_vals, cheetah_dist, "Color", "r", "LineStyle", "--");
    hold on
    title(sprintf("Index: %d", i));
end
hold off
sgtitle("Best 8 Features")

% Worst 8 (Visual)
disp("Worst 8 Visual");
disp("Index: 2,3,4,5,6,58,59,64")
disp("The worst features would be those that have the most overlap because the greater the overlap means the more similar the features between cheeath and grass.");

figure(3)
features = [2,3,4,5,6,58,59,64];
for idx=1:length(features)
    i = features(idx);
    % Getting values again 
        grass_vals = zeros(length(TrainsampleDCT_FG), 1);

    for j=1:length(TrainsampleDCT_FG)
        grass_vals(j) = TrainsampleDCT_FG(j, i);
    end
    cheetah_vals = zeros(length(TrainsampleDCT_BG), 1);
    for j=1:length(TrainsampleDCT_BG)
        cheetah_vals(j) = TrainsampleDCT_BG(j, i);
    end
    % Plottings
    grass_pi = grass_pi_res(i);
    grass_var = grass_var_res(i);
    cheetah_pi = cheetah_pi_res(i);
    cheetah_var = cheetah_var_res(i);
    
    allvals = cat(1, grass_vals, cheetah_vals);
    x_vals = min(allvals):.0001:max(allvals);
    grass_dist = gaussianPDF(x_vals, grass_pi, sqrt(grass_var));
    cheetah_dist = gaussianPDF(x_vals, cheetah_pi, sqrt(cheetah_var));
    subplot(2,4,idx)
    l1 = plot(x_vals, grass_dist, "Color", "g");
    hold on
    l2 = plot(x_vals, cheetah_dist, "Color", "r", "LineStyle", "--");
    hold on
    title(sprintf("Index: %d", i));
end
hold off
sgtitle("Worst 8 Features")

%%%%%%%%%%%%%%%%% Part C %%%%%%%%%%%%%%%%%

img = im2double(imread("cheetah.bmp"));
for i=1:10:(size(img, 1) - 8)
    for j=1:10:(size(img, 2) - 8)
       block = img(i:i+8, j:j+8);
       blockDCT = dct2(block);
       blockFlat = flatten(blockDCT);
       
       
    end
end





