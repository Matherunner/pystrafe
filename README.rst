=========================
pystrafe (very rough WIP)
=========================

**NOTE**: This is **work in progress**! The interface may change from version to
version.

A Python module of Half-Life physics routines for research and experimentation
purposes.

Install
=======

::

   $ pip install pystrafe

Examples
========

The following examples illustrate different situations one might encounter. In
each example, `pystrafe` is used to aid planning and validation of run
strategies by solving computational problems.

Jumping over a big gap
----------------------

There is a gap of 1000 units wide that can save 30s from the run if leaped
across. The difference in player position at the starting (standing) and ending
(ducking) position is merely 100 units. You are playing at 100 fps and default
settings. Unsure if a TAS bot can make the jump, let alone a human player?

.. code:: pycon

   >>> from pystrafe import motion, jumpspeed
   >>> K = motion.strafe_K_std(0.01)
   >>> dist, height = 1000, -100
   >>> gravity = 800
   >>> motion.strafe_solve_speedxi(jumpspeed, K, dist, height, gravity)
   1046.7786535278178

Looks like you need at least 1046 ups *at the moment you jump* to make it across
the gap!

**Note**: the `height` variable is declared `-100` rather than `100`, because
the final position is at a *lower* position than the starting point.

Damage boosting over a big gap
------------------------------

There is a gap 700 units wide and the solid ground ahead is 200 units below the
current position. You have very low health and a grenade, and running towards
the gap at 100 ups. How would you damage boost across the gap while *minimising
the health loss*? Boost horizontally? Boost towards the opposite edge? Boost at
an upward angle?

.. code:: pycon

   >>> from pystrafe import motion, jumpspeed
   >>> K = motion.strafe_K_std(0.001)
   >>> vel = [100, jumpspeed]
   >>> dist, height = 700, -200
   >>> gravity = 800
   >>> dv = motion.solve_boost_min_dmg(vel, K, dist, height, gravity)
   >>> dv
   [172.28574486554757, 218.8998258941578]
   >>> 
   >>> # Calculate the health required and angle of boosting!
   >>> from math import hypot, atan2, degrees
   >>> hypot(dv[0], dv[1]) / 10   # 10 because of ducking
   27.856688902374805
   >>> degrees(atan2(dv[1], dv[0]))
   51.79538244723009

Turns out you must launch yourself upwards at about 52 degrees and lose about 28
HP at the bare minimum! The answer is often slightly surprising, and non-trivial
to work out by yourself, but you can trust the results computed by `pystrafe`.

You are curious how long the jump itself will take to get to the other side.

.. code:: pycon

   >>> motions.strafe_time(dist, vel[0] + dv[0], K)
   1.5422678575586732

That is about 1.54 seconds. Now you can decide if you would like to cut this
down further by applying more damage to the boost. Remember, the about 278
damage calculated earlier is the *minimum* required!

How much armour do you need?
----------------------------

From the previous section, we computed that we need to lose 28 HP.
Unfortunately, the grenade has to be placed very close to us. You decided to
acquire some more armour to survive a closer grenade blast. How much do you
need?

.. code:: pycon

   >>> from pystrafe import damage
   >>> damage.ap_dhp_damage(28, 80)
   (25.5, 26.0, '(', ']')

We need to acquire AP in the range of (25.5, 26] to obtain the desired health
loss.

.. Ladder speeding
   ---------------
   
   You are working on a run of a Half-Life mod. There is a ladder sloped at a 60
   degrees angle that you must climb as fast as possible. You are skilled at
   looking perfectly upwards and holding A and W keys at the same time to speed
   through a ladder at 400 ups. Are you sure this is the optimal approach this time
   around?
   
   .. code:: pycon
   
      >>> from pystrafe import ladder
      >>> ladder.best_yaw()
      TODO
      >>> ladder.best_pitch()
      TODO
   
   Looks like you need BXT's `bxt_hud_viewangles` to nail down these viewangles.

Limitations
===========

There exists a perfect, minimal-time route from start to finish in any game,
including Half-Life and its expansions, known only to the gods. This Python
module cannot be used to discover that route! At least not in its entirety.

Documentation
=============

.. Visit the documentation at https://matherunner.github.io/pystrafe/.

The underlying physics is documented separately at https://www.jwchong.com/hl/.
