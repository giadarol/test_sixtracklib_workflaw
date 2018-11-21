import pickle
import pysixtracklib
import helpers as hp
import pysixtrack
import os

track_with = 'PySixtrack'
track_with = 'Sixtrack'

n_turns = 3

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
for name, etype, ele in line:
    getattr(elements, etype)(**ele._asdict())
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

    p.fromPySixTrack(part, i_part)

ps.tofile('particles.buffer')

os.system('../sixtracklib/build/examples/c99/track_io_c99 particles.buffer elements.buffer 10 0 10 1')

res = pysixtracklib.ParticlesSet.fromfile('output_particles.bin')