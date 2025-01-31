"""
Legend
------

The :meth:`pygmt.Figure.legend` method can automatically create a legend for
symbols plotted using :meth:`pygmt.Figure.plot`. Legend entries are only
created when the ``label`` parameter is used.
"""
import pygmt

fig = pygmt.Figure()

fig.basemap(projection="x2c", region=[0, 7, 3, 7], frame=True)

fig.plot(
    data="@Table_5_11.txt",
    style="c0.40c",
    fill="lightgreen",
    pen="faint",
    label="Apples",
)
fig.plot(data="@Table_5_11.txt", pen="1.5p,gray", label="My lines")
fig.plot(data="@Table_5_11.txt", style="t0.40c", fill="orange", label="Oranges")

fig.legend(position="JTR+jTR+o0.2c", box=True)

fig.show()
