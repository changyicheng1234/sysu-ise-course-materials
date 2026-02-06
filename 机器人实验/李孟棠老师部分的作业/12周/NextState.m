
function nextconf = NextState(current_conf,control,detat,max_speed)
%q = [fi,x,y,J1,J2,J3,J4,J5,cita1,cita2,cita3,cita4];
%u = [j1,j2,j3,j4,j5,citaa1,citaa2,citaa3,citaa4];
fi = current_conf(1);
l = 0.47/2;
w = 0.3/2;
r = 0.0475;
t = 1;
citaa = control(6:9); % control, 4x1
detacita = detat*citaa;



F = r/4 * [-1/(l+w) 1/(l+w) 1/(l+w) -1/(l+w);1 1 1 1; -1 1 -1 1];
Vb = F * detacita ;


w_bz = Vb(1);
v_bx = Vb(2);
v_by = Vb(3);
if w_bz == 0
    detafi_b = 0;
    detax_b =v_bx;
    detay_b = v_by;
    detaq_b = [detafi_b;detax_b;detay_b];
end
if w_bz ~= 0
    detaq_b = [w_bz;(v_bx*sin(w_bz)+v_by*(cos(w_bz) - 1))/w_bz;...
        (v_by*sin(w_bz)-v_bx*(cos(w_bz) - 1))/w_bz];
end

detaq = [1 0 0;0 cos(fi) -sin(fi);0 sin(fi) cos(fi)]*detaq_b;

q = current_conf;
q_k1 = zeros(12,1);
q_k1(1:3) = q(1:3) + detaq;
q_k1(4:8) = q(4:8) + 0;
q_k1(9:12) = q(9:12) + detacita;
nextconf = q_k1';
end


