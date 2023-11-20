import numpy as np
import pygimli as pg
from pygimli.physics import TravelTimeManager
import pygimli.physics.traveltime as tt
import pygimli.meshtools as mt

from pygimli.meshtools import quality
import pyvista as pv
import pygimli.viewer.pv
from scipy.io import loadmat
import matplotlib as mpl 

Dout = 156 
Din = Dout -10
circle_outer = mt.createCircle(pos=[0.0, 0.0], radius=Dout/2,
                               nSegments=64, marker=1,
                               markerPosition=[Dout/2*0.995, 0.0])
circle_inner = mt.createCircle(pos=[0.0, 0.0], radius=Din/2, 
                               nSegments=64, marker=2,
                               markerPosition=[Din/2*0.995, 0.0])

geom = circle_outer + circle_inner
#ax, cb = pg.show(geom, markers=True)
#fig = ax.get_figure()
#for nr, marker in enumerate(geom.regionMarkers()):
#    print('Position marker number {}:'.format(nr + 1), marker.x(), marker.y(), marker.z())
#    ax.scatter(marker.x(), marker.y(), s=(2 - nr) * 30, color='k')
#ax.set_title('marker positions - working example')
#fig.show()

#ax, _ = pg.show(geom, markers=True);
#for i, n in enumerate(geom.nodes()[:12]):
#    ax.text(n.x(), n.y(), str(i))
#    print(i, n.x(), n.y())
    
#for i in range(100, geom.nodeCount()):
#    print(i, geom.node(i).x(), geom.node(i).y())

geom.addRegionMarker([0, 0], marker=2)
#ax = pg.show(geom, markers=True)[0]

mesh = mt.createMesh(geom, quality=34.4)

print(mesh)
ax = pg.show(mesh, markers=True, showMesh=True)[0]

data = tt.load('test.txt')
for i, d in enumerate(data.sensors()):
    data.setSensor(i, d*10)

pg.viewer.mpl.drawSensors(ax, data.sensors(), diam=3, color='k')

mgr = tt.Manager(data, verbose=True)

mgr.setMesh(mesh)
#mgr.inv.setRegularization(1, fix=1/2000) # will not work
mgr.inv.setRegularization(1, background=False, single=True, startModel=1/500)
mgr.inv.setRegularization(2, background=False, startModel=1/10)
mgr.fop.setInterRegionCoupling(1, 2, weight=0.9)

velInv = mgr.invert(data, maxIter=10, lam=100, zWeight=1.0)

# mappedModel = mgr.fop.createMappedModel(velInv, 10)
# ax = pg.show(mgr.fop.mesh(), mappedModel)[0]

fig = mgr.showResultAndFit()
mgr.drawRayPaths(fig.modelAX)
