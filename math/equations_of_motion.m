clear all
syms x1 y1 x2 y2
syms x1p y1p x2p y2p
syms q1 q2 q1p q2p
syms m1 m2 l1 l2 w1 w2
syms g
syms L

T = 1/2*(m1*l1^2*q1p^2 + m2*(w1^2*q1p^2 + l2^2*q2p^2 + 2*w1*l2*q1p*q2p*cos(q1-q2)));
V = -m1*g*l1*cos(q1) - m2*g*(w1*cos(q1)+l2*cos(q2));

L = T - V;

display("L = ");
pretty(L);

dLdq1 = diff(L,q1);
dLdq2 = diff(L,q2);
dLdq1p = diff(L,q1p);
dLdq2p = diff(L,q2p);


%dtdLdq1 = -g l1 m1 q1p cos(q1) - g m2 q1p cos(q1) w1 - l2 m2 p^2 q1(t) q2(t) ?_1 (q1'(t) - q2'(t)) cos(q1(t) - q2(t)) - l2 m2 p^2 q2(t) q1'(t) ?_1 sin(q1(t) - q2(t)) - l2 m2 p^2 q1(t) q2'(t) ?_1 sin(q1(t) - q2(t))

%%
syms q1p(t) q2p(t) q1(t) q2(t)
dLdq1p = m1*q1p(t)*l1^2 + (m2*(2*q1p(t)*w1^2 + 2*l2*q2p(t)*cos(q1 - q2)*w1))/2;

dLdq2p = (m2*(2*q2p(t)*l2^2 + 2*q1p(t)*w1*cos(q1 - q2)*l2))/2;

dtdLdq1p = diff(dLdq1p,t);
dtdLdq2p = diff(dLdq2p,t);

%%
syms x1 x2 x3 x4
syms x1p y1p x2p y2p
syms q1 q2 q1p q2p q1pp q2pp
syms m1 m2 l1 l2 w1 w2
syms g
syms L
syms tal1 tal2 b1 b2

%solution drive by hand (need to do revision on web page)
dtdLdq1p = m1*l1^2*q1pp + m2*w1^2*q1pp + m2*w1*l2*q2pp*cos(q1-q2) - m2*w1*l2*q2p*sin(q1-q2)*q1p + m2*w1*l2*q2p*sin(q1-q2)*q2p;
dtdLdq2p = m2*l2^2*q2pp + m2*w1*l2*q1pp*cos(q1-q2) - m2*w1*l2*q1p*sin(q1-q2)*q1p + m2*w1*l2*q1p*sin(q1-q2)*q2p;
q_vec = [q1,q1p,q2,q2p];
x_vec = [x1,x2,x3,x4];

dLdq1 = subs(dLdq1,q_vec,x_vec);
dLdq2 = subs(dLdq2,q_vec,x_vec);
dtdLdq1p = subs(dtdLdq1p,q_vec,x_vec);
dtdLdq2p = subs(dtdLdq2p,q_vec,x_vec);

eqns = [dtdLdq1p - dLdq1 == 2*tal1+2*(w1/l1)*tal2-b1*x2 ; dtdLdq2p - dLdq2 == 2*tal2-b2*x4];
S = solve(eqns,[q1pp;q2pp]);
display("q1pp");
S.q1pp
display("q2pp");
S.q2pp
