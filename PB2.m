% Generalized Rayleigh-Ritz Method (PB2) for Natural Frequency of Regular Polygonal Plates
% Original Author: Dhairya D. Dosi, Aug 2023
% Modified for any regular polygon with arbitrary sides and side length

clear; clc;
syms x y p real;
D = 1;             % Flexural rigidity
nu = 0.3;          % Poisson's ratio
rho = 1;           % Density
d = 1;             % Thickness

%% User-defined parameters:
n_sides = 6;       % Number of polygon sides (e.g., 6 for hexagon, 5 for pentagon, etc.)
a = 1;             % Side length of polygon

%% Generate Polygon Geometry:
theta = linspace(0, 2*pi, n_sides+1);
R = a/(2*sin(pi/n_sides)); % Radius of circumscribed circle
x_poly = R*cos(theta);
y_poly = R*sin(theta);

%% Shape function (generalized):
w_poly = 1;
for i=1:n_sides
    x1 = x_poly(i); y1 = y_poly(i);
    x2 = x_poly(i+1); y2 = y_poly(i+1);
    % Equation of line segment: (y-y1)*(x2-x1)-(x-x1)*(y2-y1)=0
    edge_eq = ((y - y1)*(x2 - x1) - (x - x1)*(y2 - y1));
    w_poly = w_poly * edge_eq^2;
end

%% Assume generalized displacement function:
syms A [1 9] real;
w_trial = w_poly*(A1 + A2*x^2 + A3*y^2 + A4*x^2*y^2 + A5*x^4 + A6*y^4 + A7*x^4*y^2 + A8*x^2*y^4 + A9*x^4*y^4);

%% Strain energy and kinetic energy expressions:
del2w=((diff(w_trial,x,2)+diff(w_trial,y,2))^2) - (2*(1-nu)*((diff(w_trial,x,2)*diff(w_trial,y,2))-(diff(diff(w_trial,x),y)^2)));
k_energy= p*rho*d*w_trial^2;

%% Integration over polygon area:
pi_energy=(D/2)*int(int(del2w,y,min(y_poly),max(y_poly)),x,min(x_poly),max(x_poly));
ni_energy=(0.5)*int(int(k_energy,y,min(y_poly),max(y_poly)),x,min(x_poly),max(x_poly));

%% Rayleigh-Ritz functional:
pi_total=pi_energy+ni_energy;

%% Stationary conditions:
eqns=[];
for i=1:9
    eqns=[eqns; diff(pi_total,A(i))==0];
end

%% Solve characteristic equation:
[coeff_matrix,~]=equationsToMatrix(eqns,[A]);
char_eq=det(coeff_matrix)==0;

%% Solve for p (frequency squared):
p_sol=vpasolve(char_eq,p);
natural_freq=sqrt(double(p_sol));

disp('Approximate natural frequency:');
disp(natural_freq);