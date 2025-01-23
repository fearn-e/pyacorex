import json
import numpy as np
import os
import sys

# Require command line argument for JSON corpus file
#if len(sys.argv) < 2:
#    print(f'Usage: {sys.argv[0]} filename.wav')
#    sys.exit(-1)

# Load audio files and descriptor values from JSON corpus file
def load_acorex_corpus(json_path):
    data = None
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print(f"JSON file {sys.argv[1]} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file {sys.argv[1]}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    audio_files_JSON = data.get("fileList", [])
    corpus_values_JSON = data.get("time.raw", [])
    segment_length = int(data.get("windowFFTSize", 0))
    hop_fraction = int(data.get("hopFraction", 0))
    sample_rate = int(data.get("sampleRate", 0))

    hop_size = int(segment_length / hop_fraction)

    audio_files = []
    for file_path in audio_files_JSON:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as audio_file:
                    audio_files.append(audio_file.read())
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"File {file_path} not found.")

    corpus_values = [np.array(item) for item in corpus_values_JSON] # each numpy array is a segment x descriptor array
                                                                    # in the test corpus the descriptors are [time, umap1, umap2, umap3]

    print(f"Loaded {len(audio_files)} audio files.")
    print(f"Corpus values file count: {len(corpus_values)}")
    print(f"Total segment count: {sum([item.shape[0] for item in corpus_values])}")
    print(f"Descriptor count: {corpus_values[0].shape[1]}")
    print(f"Segment length: {segment_length}")
    print(f"Sample rate: {sample_rate}")
    print(f"Hop size: {hop_size}")
    print(f"Segment length in ms: {segment_length / sample_rate * 1000}")
    print(f"Hop size in ms: {hop_size / sample_rate * 1000}")

    return audio_files, corpus_values, segment_length, sample_rate, hop_size

import plotly.graph_objects as go

# Main function
audio_files, corpus_values, segment_length, sample_rate, hop_size = load_acorex_corpus("corpus.json")

fig = go.FigureWidget()

for i, item in enumerate(corpus_values):
    scatter = go.Scatter3d(
        x=item[:,1], y=item[:,2], z=item[:,3],
        mode='lines+markers',
        marker=dict(size=2, color=item[:,0]),
        line=dict(width=1, color=item[:,0]),
        opacity=0.5
    )
    fig.add_trace(scatter)

fig.update_layout(hovermode='closest')

scatter = fig.data[0]

# Create our callback function
def update_point(trace, points, selector):
    print(f"Selected {len(points.point_inds)} points.")
    c = list(trace.marker.color)
    s = list(trace.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
    with fig.batch_update():
        trace.marker.color = c
        trace.marker.size = s

# Attach the callback to each scatter trace
scatter.on_click(update_point)

fig.show()

# Display corpus values as a 3D point cloud in Panda3D - too complicated for now
'''
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)


app = MyApp()
app.run()
'''

# Display corpus values as a 3D point cloud in matplotlib - too slow
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()

for i, item in enumerate(corpus_values):
    ax = fig.add_subplot(1, len(corpus_values), i+1, projection='3d')
    scatter = ax.scatter(item[:,1], item[:,2], item[:,3], c=item[:,0])
    ax.set_title(f"Corpus values file {i}")
    fig.colorbar(scatter, ax=ax, label='Color by item[:,0]')

plt.show()
'''

#Display corpus values as a 3D point cloud using glfw - too complicated for now, but probably the way to go for speed and flexibility
'''
import glfw
import OpenGL.GL as gl

def main():
    audio_files, corpus_values = load_acorex_corpus(sys.argv[1])

    print(f"Loaded {len(audio_files)} audio files.")
    print(f"Corpus values file count: {len(corpus_values)}")
    for i, item in enumerate(corpus_values):
        print(f"Corpus values file {i} (segment, descriptor) count: {item.shape}")

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "PyACorEx", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Draw a sphere at each corpus value
        gl.glBegin(gl.GL_POINTS)
        for item in corpus_values[0]:
            gl.glVertex3f(item[1], item[2], item[3])
        gl.glEnd()

        glfw.swap_buffers(window)

    glfw.terminate()

main()
'''