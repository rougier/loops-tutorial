import numpy as np
from vispy import app
from vispy import gloo
from vispy.gloo import gl

app.use('glfw')


vertex = """
attribute float x;
attribute float y;
void main (void)
{
    gl_Position = vec4(x, y, 0.0, 1.0);
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

class Window(app.Canvas):
    def __init__(self, n=50):
        app.Canvas.__init__(self)
        gl.glClearColor(1,1,1,1)

        self.program1 = gloo.Program(vertex, fragment, n)
        self.program1['x'] = np.linspace(-1.0, +1.0, n)
        self.program1['y'] = +0.5 + np.random.uniform(-0.25, +0.25, n)

        self.program2 = gloo.Program(vertex, fragment, n)
        self.program2['x'] = np.linspace(-1.0, +1.0, n)
        self.program2['y'] = -0.5 + np.random.uniform(-0.25, +0.25, n)

        self._timer = app.Timer(1.0/60)
        self._timer.connect(self.on_timer)
        self._timer.start()

    def on_resize(self, event):
        gl.glViewport(0, 0, event.size[0], event.size[1])

    def on_draw(self, event):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.program1.draw(gl.GL_LINE_STRIP)
        self.program2.draw(gl.GL_LINE_STRIP)

    def on_timer(self, event):
        n = self.program1['y'].size
        self.program1['y'] = +0.5 + np.random.uniform(-0.25, +0.25, n)

        n = self.program2['y'].size
        self.program2['y'] = -0.5 + np.random.uniform(-0.25, +0.25, n)

        self.update()


window = Window(n=100)
window.show()
app.run()
