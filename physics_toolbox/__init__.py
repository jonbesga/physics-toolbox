from math import sin, cos, radians, sqrt


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({},{},{})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "Point({},{},{})".format(self.x, self.y, self.z)


class Vector:
    def __init__(self, end, origin=Point(0, 0, 0)):
        self.origin = origin
        self.end = end

    @property
    def magnitude(self):
        return sqrt(
            (self.end.x - self.origin.x) ** 2
            + (self.end.y - self.origin.y) ** 2
            + (self.end.z - self.origin.z) ** 2
        )

    @property
    def x(self):
        return self.end.x - self.origin.x

    @property
    def y(self):
        return self.end.y - self.origin.y

    @property
    def z(self):
        return self.end.z - self.origin.z


class Body:
    def __init__(
        self,
        point,
        mass=0,
        weight=None,
        velocity=Vector(Point(0, 0, 0)),
        acc=Point(0, 0, 0),
        g=9.80,
        surface=None,
    ):
        self.g = g

        if weight:
            if not isinstance(weight, (int, float)):
                raise TypeError("mass needs to be a float or int")
            self.mass = weight / self.g
        elif mass:
            if not isinstance(mass, (int, float)):
                raise TypeError("mass needs to be a float or int")
            self.mass = mass

        if not isinstance(point, Point):
            raise TypeError("point needs to be an instance of Point class")
        self.pos = point

        if velocity and not isinstance(velocity, Vector):
            raise TypeError("velocity needs to be an instance of Vector class")
        self._velocity = velocity
        self.acc = acc

        self.surface = surface

    @property
    def initial_pos(self):
        return self.pos

    @property
    def initial_vel(self):
        return self._velocity

    @property
    def initial_acc(self):
        return self.acc

    @property
    def weight(self):
        return self.mass * self.g

    @property
    def weight_y(self):
        weigth = self.mass * self.g
        if self.surface:
            if self.surface.inclination != 0:
                return weigth * cos(self.surface.inclination_rad)
        return self.weight

    @property
    def weight_x(self):
        weigth = self.mass * self.g
        if self.surface:
            if self.surface.inclination != 0:
                return weigth * sin(self.surface.inclination_rad)
        return self.weight

    @property
    def normal_force(self):
        if self.surface:
            return self.weight_y
        return None

    @property
    def friction_force(self):
        if self.surface:
            return self.surface.friction_coefficient * self.normal_force
        return None

    def work_other_forces(self, s):
        ff = self.friction_force
        if ff:
            return ff * s
        return None

    @property
    def potential_energy(self):
        return self.mass * self.g * self.pos.y

    @property
    def kinetic_energy(self):
        return 1 / 2 * self.mass * self.velocity ** 2

    @property
    def total_mechanical_energy(self):
        return self.kinetic_energy + self.potential_energy

    @property
    def velocity(self):
        return None if not self._velocity else self._velocity.magnitude

    @velocity.setter
    def set_velocity(self, value):
        self._velocity = value

    def find_pos(self, t=0):
        x = (
            self.initial_pos.x
            + self.initial_vel.x * t
            + (1 / 2) * self.initial_acc.x * t ** 2
        )
        y = self.initial_pos.y + self.initial_vel.y * t - (1 / 2) * self.g * t ** 2
        return x, y

    def __repr__(self):
        return "Body({})".format(str(self.pos))


class Ramp:
    def __init__(
        self, length=0, base=0, height=0, inclination=0, friction_coefficient=None
    ):
        self.inclination = inclination
        self.friction_coefficient = friction_coefficient

        if self.inclination > 0:
            if length:
                self.length = length
                self.height = self.length * sin(self.inclination_rad)
                self.base = self.length * cos(self.inclination_rad)
            if base:
                self.base = base
                self.length = self.base / cos(self.inclination_rad)
                self.height = self.length * cos(self.inclination_rad)
            if height:
                self.height = height
                self.length = self.base / sin(self.inclination_rad)
                self.base = self.length * sin(self.inclination_rad)
        else:
            self.length = length
            self.base = length
            self.height = height

    @property
    def inclination_rad(self):
        return radians(self.inclination)
