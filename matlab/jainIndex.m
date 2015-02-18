function index = jainIndex(x)
n = length(x);
index = sum(x)^2/(n*sum(x.^2));