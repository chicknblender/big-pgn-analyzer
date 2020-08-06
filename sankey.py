import sankeyfx
import plotly.graph_objects as go
import os
import plotly.io
import folder

threshold = 0.00

nodes = sankeyfx.get_nodes('../scandi/2. exd5/2... Nf6/3. d4', threshold)

labels = []
sources = []
targets = []
values = []
win_difs = []
xvals = []
yvals = []

for n in nodes:
    labels.append(n['label'])
    sources.append(n['source'])
    targets.append(n['target'])
    values.append(n['value'])
    win_difs.append(n['win_dif'])
    xvals.append(n['x'])
    yvals.append(n['y'])
    

# this is for determining the flow colors
extreme = 30 # if win_dif >= extreme, color will be white. if win_dif <= -extreme, color = black
colorlist = []
for n in win_difs:
    c = int(n * 128/extreme + 128)
    if c > 255:
        c = 255
    if c < 0:
        c = 0
    c = str(c)
    colorlist.append('rgb(' + c + ',' + c + ',' + c + ')')

fig = go.Figure(data=[go.Sankey(
    arrangement = "perpendicular",
    orientation = 'h',
    node = dict(
      pad = 20,
      thickness = 10,
      line = dict(color = "black", width = 0.5),
      label = labels,
      color = 'rgb(181,136,99)',
      x = xvals,
      y = yvals
    ),
    link = dict(
      source = sources,
      target = targets,
      value = values,
      color = colorlist
  ))])

fig.update_layout(title_text='',
                plot_bgcolor='rgb(240,217,181)',
                paper_bgcolor='rgb(240,217,181)',
                font_size=12)
fig.show()
# fig.write_image("images/fig1.png")
