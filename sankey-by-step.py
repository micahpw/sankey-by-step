#%%
import pandas as pd

df = pd.read_csv('./test.csv')
df.head()

#%%
# Determine Initial Sources 
# map to step == 0.
max_step = df.groupby('target')[['step']].max()
step_map = dict(zip(max_step.index, max_step.step))
df['source_step'] = df['source'].map(step_map).fillna(0).astype(int)

#%%
# Get a list of all unique labels..
# to index off of.
labels = pd.concat([
  df['source'],
  df['target']
]).drop_duplicates().to_frame().rename(columns={0:'label'})

labels = labels.reset_index().drop(columns=['index'])
labels
#%%
# Create a dict map from the target/source name to the 
# corresponding index of the name in the list of labels
label_map = dict(zip(labels['label'], labels.index))
print(label_map)

#%%
# Map the label to the appropriate index
df['target_index'] = df['target'].map(label_map)
df['source_index'] = df['source'].map(label_map)


# %%
import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = labels['label'],
      color = "blue",
      x=df['source_step'].apply(lambda x: x*0.2)
    ),
    link = dict(
      source = df['source_index'], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = df['target_index'],#targets,
      value = df['value'],
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()
# %%
