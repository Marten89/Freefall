"""Freefall is a model for falling objects.

An object is created with a few attributes specified. The model can then be
used to simulate what would happen to the object if released at some height,
considering the opposing forces of weight and air resistance.

Air resistance, or drag force, is modelled as 0.5*C*p*A*v^2 where A is the
cross sectional area of the object, p (rho) is the air density, v is the
current velocity and C is a coefficient related to the shape of the object.
This coefficient is usually determined experimentally in wind tunnels. C is
approximately 1.0 for a horizontal human. The drag force is proportinal to the
square of the velocity, while the force of the weight is a constant m*g, the
object mass times the gravity acceleration. When a falling object's velocity
becomes high enough, it will stop accelerating due to the increased drag and
continue it's fall at it's terminal velocity. Freefall can for example be used
to find an objects terminal velocity, and see if a given height is enough to
reach it before it lands. This model does not account for the variations in
air density and gravity depending on altitude. Calculations are done with a
time step of 0.01 seconds.
"""

class Freefall:
    """This class implements a model of an object in free fall."""

    def __init__(self, mass, area, drag_coef=1, density=1.2, gravity=9.81):
        """Construct an model taking the mass in kg and cross sectional area in
        m^3. They need to be larger than 0. Additional optional arguments are:

        - The drag coefficient C has a value larger than 0 and less than 2. It
          has the default value 1.0, representing a human in horizontal
          position.
        - The air density p needs to be non-negative. It has the default value
          1.20 kg/(m^3), representing the density at 1 atm pressure and 20
          degrees celsius.
        - The gravity g needs to be larger than 0. It has the default value
          9.81 m/(s^2), representing standard gravity at the surface of the
          earth.

        Each argument can be given as int or float. Other types will cause a
        TypeError. Values outside the specified ranges will cause a ValueError.
        """

        for arg in [mass, area, drag_coef, density, gravity]:
            if not isinstance(arg, (int, float)):
                raise TypeError("All arguments must be of type int or float")
        for arg in [mass, area, drag_coef, gravity]:
            if arg <= 0:
                raise ValueError("Argument is outside specified range")
        if drag_coef >= 2 or density < 0:
            raise ValueError("Argument is outside specified range")
        
        self._m = mass       #Mass in kg
        self._A = area       #Area in m^2
        self._C = drag_coef  #Drag coefficient
        self._p = density    #Density of air in kg/(m^3)
        self._g = gravity    #Gravity acceleration in m/(s^2)

    def set_drag_coef(self, drag_coef):
        """Modify drag coefficient C to a float or int larger than 0 and
        less than 2. Value outside of that range causes ValueError. Wrong
        type causes TypeError.
        """
        if not isinstance(drag_coef, (int, float)):
            raise TypeError("C must be of type int or float")
        elif drag_coef <= 0 or drag_coef >= 2:
            raise ValueError("C must be larger than 0 and less than 2")
        self._C = drag_coef

    def set_density(self, density):
        """Modify air density p to a non-negative float or int in kg/(m^3).
        Wrong range causes ValueError. Wrong type causes TypeError.
        """
        if not isinstance(density, (int, float)):
            raise TypeError("p must be of type int or float")
        elif density < 0:
            raise ValueError("p must be non-negative")
        self._p = density

    def set_gravity(self, gravity):
        """Modify gravity g to a positive float or int in m/(s^2). A zero or
        negative g causes ValueError. Wrong type causes TypeError.
        """
        if not isinstance(gravity, (int, float)):
            raise TypeError("g must be of type int or float")
        elif gravity <= 0:
            raise ValueError("g must be larger than 0")
        self._g = gravity

    def set_size(self, mass, area):
        """Modify the mass in kg and cross sectional area in m^3 as positive
        int or float parameters. Zero or negative values causes ValueError.
        Wrong type causes TypeError.
        """
        if not isinstance(mass, (int, float)) or not isinstance(area, (int, float)):
            raise TypeError("A and m must be of type int or float")
        elif mass <= 0 or area <= 0:
            raise ValueError("A and m must be larger than 0")
        self._m = mass
        self._A = area

    def properties(self):
        """Return a dict with the models properties (mass, area,
        drag coefficient, air density, and gravity) as keys and their
        current values in SI-units as values.
        """
        return {"m (kg)": self._m, "A (m^2)": self._A, "C": self._C,
                "p (kg/(m^3))": self._p, "g (m/(s^2))": self._g}        

    def terminal(self):
        """Calculate and return the terminal velocity of the object in m/s
        as a float rounded to two decimals. Return None if air density p = 0.
        """
        if self._p == 0:
            return None
        v_term = ((2*self._m*self._g)/(self._p*self._C*self._A))**0.5
        return round(v_term, 2)

    def air_time(self, height):
        """Calculate and return the time until the object hits the ground
        when released from a height. The time is in s and represented as a
        float rounded to two decimals. The height is in m and is input as a
        positive int or float. Zero or negative values causes ValueError.
        Other types causes TypeError.
        """
        if not isinstance(height, (int, float)):
            raise TypeError("Height must be of type int or float")
        elif height <= 0:
            raise ValueError("Height must be larger than 0")
        t_air = self._calculator(height)[0][-1]
        return round(t_air, 2)

    def landing_speed(self, height):
        """Calculate and return the speed at impact with the ground when
        released from a height. The speed is in m/s and represented as a
        float rounded to two decimals. The height is in m and is input as a
        positive int or float. Zero or negative values causes ValueError.
        Other types causes TypeError.
        """
        if not isinstance(height, (int, float)):
            raise TypeError("Height must be of type int or float")
        elif height <= 0:
            raise ValueError("Height must be larger than 0")
        v_land = self._calculator(height)[1][-1]
        return round(v_land, 2)

    def _calculator(self, height):
        v = 0
        t = 0
        step = 0.01
        time_vector = [t]
        speed_vector = [v]

        while height > 0:
            drag = 0.5*self._C*self._p*self._A*v**2
            acc = self._g-drag/self._m
            v = v+acc*step
            speed_vector.append(v)
            height = height-v*step
            t += step
            time_vector.append(t)
        return(time_vector, speed_vector)          
