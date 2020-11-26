import glooey
import numpy as np
import pyglet
import trimesh

from pyglet.gl import *  # NOQA


class SceneGroup(pyglet.graphics.Group):

    def __init__(self, rect, parent=None):
        super().__init__(parent)
        self.rect = rect

    def set_state(self):
        glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_SCISSOR_TEST)
        glScissor(
            int(self.rect.left),
            int(self.rect.bottom),
            int(self.rect.width),
            int(self.rect.height),
        )

        self._mode = (GLint)()
        glGetIntegerv(GL_MATRIX_MODE, self._mode)
        self._viewport = (GLint * 4)()
        glGetIntegerv(GL_VIEWPORT, self._viewport)

        left, bottom = int(self.rect.left), int(self.rect.bottom)
        width, height = int(self.rect.width), int(self.rect.height)
        glViewport(left, bottom, width, height)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluPerspective(60, width / height, 0.01, 1000.0)
        glMatrixMode(GL_MODELVIEW)

        glClearColor(*[.99, .99, .99, 1.0])

        self._enable_depth()
        self._enable_color_material()
        self._enable_blending()
        self._enable_smooth_lines()
        self._enable_lighting()
        self._clear_buffers()

    def unset_state(self):
        glClearColor(*[0, 0, 0, 0])

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(self._mode.value)
        glViewport(
            self._viewport[0],
            self._viewport[1],
            self._viewport[2],
            self._viewport[3],
        )

        glPopAttrib()

    def _enable_depth(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glDepthRange(0.0, 100.0)
        glDepthFunc(GL_LEQUAL)
        glClearDepth(1.0)

    def _enable_color_material(self):
        from trimesh.rendering import vector_to_gl as v

        glEnable(GL_COLOR_MATERIAL)

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glShadeModel(GL_SMOOTH)

        glMaterialfv(GL_FRONT, GL_AMBIENT, v(0.192250, 0.192250, 0.192250))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, v(0.507540, 0.507540, 0.507540))
        glMaterialfv(GL_FRONT, GL_SPECULAR, v(0.5082730, .5082730, .5082730))
        glMaterialf(GL_FRONT, GL_SHININESS, 0.4 * 128.0)

    def _enable_blending(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _enable_smooth_lines(self):
        # Make things generally less ugly.
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(1.5)
        glPointSize(4)

    def _enable_lighting(self):
        from trimesh.rendering import vector_to_gl as v

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, v(0.5, 0.5, 0.5, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, v(1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, v(1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, v(0.0, 0.0, 0.0, 1.0))

    def _clear_buffers(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


class MeshGroup(pyglet.graphics.Group):

    def __init__(self, transform=None, view_transform=None, parent=None):
        super().__init__(parent)
        if transform is None:
            transform = np.eye(4)
        self.transform = transform
        if view_transform is None:
            view_transform = np.eye(4)
        self.view_transform = view_transform

    def set_state(self):
        from trimesh.rendering import matrix_to_gl

        glPushMatrix()

        glLoadIdentity()
        glMultMatrixf(matrix_to_gl(self.view_transform))
        glMultMatrixf(matrix_to_gl(self.transform))

    def unset_state(self):
        glPopMatrix()


class MeshWidget(glooey.Widget):

    # I suppose this should take a scene object rather than a mesh, but I
    # couldn't really figure out how to make a scene object.

    def __init__(self, mesh, transform):
        super().__init__()
        self.mesh = mesh
        self.transform = transform
        self.vertex_list = None
        self.mesh_group = None

        from trimesh.transformations import Arcball

        self.view = {'translation': np.zeros(3),
                     'center': self.mesh.centroid,
                     'scale': self.mesh.scale,
                     'ball': Arcball()}

    def do_claim(self):
        return 0, 0

    def do_regroup(self):
        if self.vertex_list is not None:
            self.mesh_group = MeshGroup(
                transform=transform,
                view_transform=view_to_transform(self.view),
                parent=SceneGroup(rect=self.rect, parent=self.group),
            )
            self.batch.migrate(
                self.vertex_list,
                GL_TRIANGLES,
                self.mesh_group,
                self.batch,
            )

    def do_draw(self):
        from trimesh.rendering import mesh_to_vertexlist

        # Because the vertex list can't change, we don't need to do anything if
        # the vertex list is already set.
        if self.vertex_list is None:
            self.mesh_group = MeshGroup(
                transform=self.transform,
                view_transform=view_to_transform(self.view),
                parent=SceneGroup(rect=self.rect, parent=self.group),
            )
            args = mesh_to_vertexlist(self.mesh, group=self.mesh_group)
            self.vertex_list = self.batch.add_indexed(*args)

    def do_undraw(self):
        if self.vertex_list is not None:
            self.vertex_list.delete()
            self.vertex_list = None

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.view['ball'].down([x, -y])
        if self.mesh_group:
            self.mesh_group.view_transform = view_to_transform(self.view)
        self._draw()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # detect crossing edge between widgets
        x_prev = x - dx
        y_prev = y - dy
        left, bottom = self.rect.left, self.rect.bottom
        width, height = self.rect.width, self.rect.height
        if not (left <= x_prev <= left + width) or \
                not (bottom <= y_prev <= bottom + height):
            self.view['ball'].down([x, y])

        # left mouse button, with control key down (pan)
        if (buttons == pyglet.window.mouse.LEFT) and \
                (modifiers & pyglet.window.key.MOD_CTRL):
            delta = [dx / self.rect.width, dy / self.rect.height]
            self.view['translation'][:2] += delta
        # left mouse button, no modifier keys pressed (rotate)
        elif (buttons == pyglet.window.mouse.LEFT):
            self.view['ball'].drag([x, -y])
        if self.mesh_group:
            self.mesh_group.view_transform = view_to_transform(self.view)
        self._draw()


def view_to_transform(view):
    transform = view['ball'].matrix()
    transform[:3, 3] = view['center']
    transform[:3, 3] -= np.dot(transform[:3, :3], view['center'])
    transform[:3, 3] += view['translation'] * view['scale']
    return transform


def main(mesh, mesh1, mesh2, mesh3, mesh4, mesh5):
    import trimesh.transformations as tf

    window = pyglet.window.Window(width=1200, height=125)
    gui = glooey.Gui(window)

    hbox = glooey.HBox()

    t = tf.translation_matrix([0, 0, -1])

    hbox.add(MeshWidget(mesh, transform=t))

    hbox.add(
        glooey.Placeholder(min_width=5, min_height=125, color=(255, 0, 0)),
        size=0
    )

    hbox.add(MeshWidget(mesh1, transform=t))
    
    hbox.add(
        glooey.Placeholder(min_width=5, min_height=125, color=(0, 0, 0)),
        size=0
    )
    
    hbox.add(MeshWidget(mesh2, transform=t))
    
    hbox.add(
        glooey.Placeholder(min_width=5, min_height=125, color=(0, 0, 0)),
        size=0
    )
    
    hbox.add(MeshWidget(mesh3, transform=t))
    
    hbox.add(
        glooey.Placeholder(min_width=5, min_height=125, color=(0, 0, 0)),
        size=0
    )
    
    hbox.add(MeshWidget(mesh4, transform=t))
    
    hbox.add(
        glooey.Placeholder(min_width=5, min_height=125, color=(0, 0, 0)),
        size=0
    )
    
    hbox.add(MeshWidget(mesh5, transform=t))

    gui.add(hbox)

    pyglet.app.run()


# if __name__ == '__main__':
#     main()
