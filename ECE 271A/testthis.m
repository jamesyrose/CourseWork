load('TrainingSamplesDCT_8.mat')
nbg = size(TrainsampleDCT_BG, 1);
nfg = size(TrainsampleDCT_FG, 1);

for i=1:64
    bg = zeros(nbg, 1);
    for j=1:nbg
        bg(j) = 1 + TrainsampleDCT_BG(j, i);
    end
    fg = zeros(nfg,1);
    for j=1:nfg
        fg(j) = 1 + TrainsampleDCT_FG(j, i);
    end
    subplot(8, 8, i)
    histogram(fg,'Normalization','probability', ...
                    'facealpha',.5,'edgecolor','none');
    hold on
    histogram(bg,'Normalization','probability', ...
                    'facealpha',.5,'edgecolor','none');
    hold on
end
hold off