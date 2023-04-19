# Unit test

import freefall
step = 0.01
model = freefall.Freefall(85, 0.7)

# test setters and properties()
def test_properties():
    props = model.properties()
    i = 0
    for param in p:
        assert props.get(keys[i]) == param
        i += 1
keys = ["m (kg)", "A (m^2)", "C", "p (kg/(m^3))", "g (m/(s^2))"]
p = [85, 0.7, 1, 1.2, 9.81]
test_properties()
p = [80, 0.6, 0.7, 1, 10]
model.set_size(p[0], p[1])
model.set_drag_coef(p[2])
model.set_density(p[3])
model.set_gravity(p[4])
test_properties()

# test terminal()
assert model.terminal() == round(((2*p[0]*p[4])/(p[3]*p[2]*p[1]))**0.5, 2) #equation for terminal velocity
model.set_size(1e-10, 1e10)
assert model.terminal() == 0 #terminal velocity approaches 0 when object density approaches 0
model.set_density(0)
assert model.terminal() == None #there is no terminal velocity when there is no air resistance

# test air_time()
model = freefall.Freefall(85, 0.7)
p = [85, 0.7, 1, 1.2, 9.81]
previous = model.air_time(0.01)
for height in [0.1, 0.2, 1, 99.99, 100, 1000]:
    current = model.air_time(height)
    assert current >= previous #air time never decreases when height increases
    previous = current
assert model.air_time(1e-10) == step #air time is one timestep when height approaches 0
assert model.air_time(1e6) == model.air_time(1e6) #function gives same output for same argument
model.set_gravity(1e10)
assert model.air_time(1000) == step #air time is one timestep when gravity approaches infinity
model.set_gravity(p[4])
model.set_density(0)
for height in [0.1, 0.2, 1, 99.99, 100, 1000]:
    assert model.air_time(height) == round(((2*height/p[4])**0.5), 2) #t = (2s/a)^2 when there is no air resistance

# test landing_speed()
model = freefall.Freefall(85, 0.7)
p = [85, 0.7, 1, 1.2, 9.81]
previous = model.landing_speed(0.01)
for height in [0.1, 0.2, 1, 99.99, 100, 1000]:
    current = model.landing_speed(height)
    assert current >= previous #landing speed never decreases when height increases
    previous = current
assert model.landing_speed(350) == model.landing_speed(350) #function gives same output for same argument
assert model.landing_speed(1e-10) == round(p[4]*step, 2) #landing speed is gravity*timestep when height approaches 0
assert model.landing_speed(1000) == model.terminal() #landing speed is equal to terminal velocity for high heights
assert model.landing_speed(10) < model.terminal() #landing speed is lower than terminal velocity for low heights
