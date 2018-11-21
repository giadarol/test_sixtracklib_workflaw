import pickle
import pysixtracklib
import helpers as hp
import pysixtrack
import os
import numpy as np

track_with = 'PySixtrack'
track_with = 'Sixtrack'

n_turns = 10

with open('line.pkl', 'rb') as fid:
    line = pickle.load(fid)

with open('particle_on_CO.pkl', 'rb') as fid:
    partCO = pickle.load(fid)

with open('DpxDpy_for_footprint.pkl', 'rb') as fid:
    temp_data = pickle.load(fid)

xy_norm = temp_data['xy_norm']
DpxDpy_wrt_CO = temp_data['DpxDpy_wrt_CO']

part = pysixtrack.Particles(**partCO)

#-----------------------------------------------------------------

Dx_wrt_CO_m, Dpx_wrt_CO_rad,\
    Dy_wrt_CO_m, Dpy_wrt_CO_rad,\
    Dsigma_wrt_CO_m, Ddelta_wrt_CO = hp.vectorize_all_coords(
        Dx_wrt_CO_m=0., Dpx_wrt_CO_rad=DpxDpy_wrt_CO[:, :, 0].flatten(),
        Dy_wrt_CO_m=0., Dpy_wrt_CO_rad=DpxDpy_wrt_CO[:, :, 1].flatten(),
        Dsigma_wrt_CO_m=0., Ddelta_wrt_CO=0.)

elements = pysixtracklib.Elements.fromline(line)
# for name, etype, ele in line:
#     getattr(elements, etype)(**ele._asdict())
elements.tofile("elements.buffer")

n_part = len(Dx_wrt_CO_m)

# Build PyST particle

ps = pysixtracklib.ParticlesSet()
p = ps.Particles(num_particles=n_part)

for i_part in range(n_part):

    part = pysixtrack.Particles(**partCO)
    part.x += Dx_wrt_CO_m[i_part]
    part.px += Dpx_wrt_CO_rad[i_part]
    part.y += Dy_wrt_CO_m[i_part]
    part.py += Dpy_wrt_CO_rad[i_part]
    part.sigma += Dsigma_wrt_CO_m[i_part]
    part.delta += Ddelta_wrt_CO[i_part]

    part.partid = i_part
    part.state = 1

    p.fromPySixTrack(part, i_part)

ps.tofile('particles.buffer')

os.system('../sixtracklib/build/examples/c99/track_io_c99 particles.buffer elements.buffer %d 0 %d 1'%(n_turns, n_turns))

# res = pysixtracklib.ParticlesSet.fromfile('particles.buffer')
res = pysixtracklib.ParticlesSet.fromfile('output_particles.bin')


x_tbt = []
px_tbt = []
y_tbt = []
py_tbt = []
sigma_tbt = []
delta_tbt = []
for i_turn in range(n_turns):

    x_tbt.append(res.particles[i_turn].x.copy())
    px_tbt.append(res.particles[i_turn].px.copy())
    y_tbt.append(res.particles[i_turn].y.copy())
    py_tbt.append(res.particles[i_turn].py.copy())
    sigma_tbt.append(res.particles[i_turn].sigma.copy())
    delta_tbt.append(res.particles[i_turn].delta.copy())

x_tbt = np.array(x_tbt)
px_tbt = np.array(px_tbt)
y_tbt = np.array(y_tbt)
py_tbt = np.array(py_tbt)
sigma_tbt = np.array(sigma_tbt)
delta_tbt = np.array(delta_tbt)
