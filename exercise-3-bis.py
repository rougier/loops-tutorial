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
varying float v_a;
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

class Window(app.Canvas):
    def __init__(self, n=50):
        app.Canvas.__init__(self)
        self.program = gloo.Program(vertex, fragment, n)
        gl.glClearColor(1,1,1,1)

        self.xdata = np.zeros(n, [('y', np.float32, 1)])
        self.xdata[...] = np.linspace(-1.0, +1.0, n)
        self.vxdata = gloo.VertexBuffer(self.xdata)
        self.program['x'] = self.vxdata

        self.ydata = np.zeros(n, [('x', np.float32, 1)])
        self.ydata[...] = np.random.uniform(-0.5, +0.5, n).astype(np.float32)
        self.vydata = gloo.VertexBuffer(self.ydata)
        self.program['y'] = self.vydata

        self._timer = app.Timer(1.0/60)
        self._timer.connect(self.on_timer)
        self._timer.start()

        self.index = 0

    def on_resize(self, event):
        gl.glViewport(0, 0, event.size[0], event.size[1])

    def on_draw(self, event):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.program.draw(gl.GL_LINE_STRIP)

    def on_timer(self, event):
        n = self.ydata.size
        self.index = (self.index+1) % n
        self.vydata[self.index] = (np.random.uniform(-0.5, +0.5),)
        self.update()


window = Window(n=256)
window.show()
app.run()
