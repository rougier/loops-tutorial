import numpy as np
from vispy import app
from vispy import gloo
from vispy.gloo import gl


n = 100
position = np.zeros((2*n, 2)).astype(np.float32)
position[:,0] = np.repeat(np.linspace(-1, 1, n), 2)
position[::2,1] = -.2
position[1::2,1] = .2
color = np.linspace(0., 1., 2*n).astype(np.float32)

vertex = """
const float M_PI = 3.14159265358979323846;

attribute vec2 a_position;

attribute float a_color;
varying float v_color;

uniform float u_time;

void main (void) {
    float x = a_position.x;
    float y = a_position.y + .1 * cos(2.0*M_PI*(u_time-.5*x));

    gl_Position = vec4(x, y, 0.0, 1.0);
    v_color = a_color;
}
"""

fragment = """

uniform float u_time;

varying float v_color;

void main()
{
    gl_FragColor = vec4(1.0, v_color, 0.0, 1.0);
}
"""

class Canvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self)
        self.program = gloo.Program(vertex, fragment)
        self.program['a_position'] = gloo.VertexBuffer(position)
        self.program['a_color'] = gloo.VertexBuffer(color)

        self._timer = app.Timer(1.0 / 60)
        self._timer.connect(self.on_timer)
        self._timer.start()

    def on_resize(self, event):
        gl.glViewport(0, 0, event.size[0], event.size[1])

    def on_draw(self, event):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.program.draw('triangle_strip')

    def on_timer(self, event):
        self.program['u_time'] = event.iteration * 1./60
        self.update()

c = Canvas()
c.show()
app.run()
