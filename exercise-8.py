import numpy as np
from vispy import app
from vispy import gloo
from vispy.gloo import gl

app.use('glfw')


vertex = """
attribute float x;
attribute float y;
attribute float i;
attribute float a;

varying float v_a;
varying float v_i;
void main (void)
{
    v_i = i;
    v_a = a;
    gl_Position = vec4(x, 1.0 - 1.0/100.0- i/50.0 +y, 0.0, 1.0);
}
"""

fragment = """
varying float v_a;
varying float v_i;
void main()
{
    if (fract(v_i) > 0.0)
        discard;
    gl_FragColor = vec4(1.0-v_a);
}
"""

class Window(app.Canvas):
    def __init__(self, n=50):
        app.Canvas.__init__(self, size=(1000,500))
        self.program = gloo.Program(vertex, fragment)
        gl.glClearColor(1,1,1,1)
        self.data = np.zeros((100,n), [('x', np.float32, 1),
                                       ('y', np.float32, 1),
                                       ('a', np.float32, 1),
                                       ('i', np.float32, 1)])

        self.data['x'] = np.linspace(-1.0, +1.0, n)
        self.data['y'] = np.random.uniform(-0.01, +0.01, (100,n))
        self.data['a'] = np.linspace(0.0, +1.0, n)
        self.data['i'] = np.repeat(np.arange(100),n).reshape(100,n)

        self.vdata = gloo.VertexBuffer(self.data)
        self.program.bind(self.vdata)

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
        n = self.data.shape[-1]
        self.data['a'] -= 1.0/n
        self.index = (self.index+1) % n
        self.data['y'][:,self.index] = np.random.uniform(-0.01, +0.01,100)
        self.data['a'][:,self.index] = 1.0
        self.vdata.set_data(self.data)
        self.update()

window = Window(n=500)
window.show()
app.run()
