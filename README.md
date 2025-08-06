SCOUT OPTIMIZER - USER DOCUMENTATION
====================================

OVERVIEW
--------
Scout Optimizer is a high-performance route planning tool for EVE Frontier, designed to find the shortest possible travel path between a large number of solar systems. You provide a starting system and a maximum radius, and the application calculates the most efficient route that visits every system in that range, saving you time and jumps.


HOW IT WORKS: A TWO-STAGE PROCESS
---------------------------------
The application uses a sophisticated, two-stage process to find the optimal route. Think of it like a ball rolling down a bumpy hill trying to find the absolute lowest point.

1. The Baseline Route: When you first click "Calculate," the app instantly computes a very good "first guess" route. It does this using fast, smart algorithms (Nearest Neighbor and 2-Opt) that untangle any obvious crossings. This is like quickly rolling the ball into a deep valley on the hill.

2. Iterative Deep Search: After the baseline is found, the app begins its main work. Using all of your computer's CPU cores in parallel, it performs a series of Passes. In each pass:
    * The current best route is sent to each CPU core.
    * Each core "shakes up" its version of the route slightly and then spends the specified Time per Pass using an advanced algorithm (Simulated Annealing) to try and find improvements. This is like shaking the ground to see if the ball can settle into an even lower point in the valley.
    * At the end of the pass, the best result from all cores is chosen as the new champion, and the process repeats.

This iterative method ensures the application thoroughly explores all possibilities to refine the route to be as short as possible.


HOW TO USE THE APPLICATION
--------------------------
Using the optimizer is a simple four-step process.

1. Enter Start System
This is your starting point. The final optimized route will always begin here. The input is not case-sensitive, so entering "jita" will work the same as "Jita".

2. Enter Max Radius (LY)
This is the maximum distance in light-years from your start system. The optimizer will find all systems within this radius and include them in the route calculation.

3. Set Optimization Parameters
These two fields control the depth of the deep search.
* Passes: The number of refinement rounds the algorithm will perform. For complex routes with many systems, more passes increase the chance of finding a better solution.
* Time/Pass (s): The number of seconds each CPU core will spend searching for improvements during a single pass. A larger number of systems requires more time per pass to be effective. The application will show a recommended minimum time next to this field after it finds the systems in your radius.

4. Calculate & Review
* Calculate Optimal Route: Click this to begin a fresh calculation. The button will be disabled while it works and will show a running log of the best distance found after each pass.
* Continue Optimization: After a calculation is finished, the button will change to this. Clicking it will run a new set of passes starting from the previously found best route, allowing you to dedicate more time to the search without starting from scratch.
* Stop Calculation: While a calculation is running, the button will change to "Stop." You can click this at any time to gracefully interrupt the process between passes if you see the route has stopped improving.


RECOMMENDED SETTINGS
--------------------
For the best results, you should adjust the Passes and Time per Pass based on the number of systems in your route. Here are some good starting points:

Number of Systems | Time per Pass (sec) | Number of Passes | Rationale
------------------|---------------------|------------------|--------------------------------------------------------------------
~30               | 5                   | 3                | The problem is relatively simple. Converges fast.
~50               | 5-7                 | 4                | A good balance of speed and quality for a typical-sized route.
~70               | 7-10                | 5                | Each core needs more time to refine the more complex route.
~100              | 10-12               | 6-8              | Significantly harder. More time and passes are needed.
~150              | 12-15               | 8-10             | Longer passes are essential to untangle complex route "knots".
~200+             | 15-20+              | 10-15+           | A difficult problem that benefits from a much longer search.


FOR THE BEST POSSIBLE RESULTS
-----------------------------
The best strategy is to watch the output log. If you see that the "best distance" is still decreasing on the final pass, it means further improvements are likely. In that case, simply click the "Continue Optimization" button to run another set of passes. Repeat this process until you see the distance plateau for several passes in a row—that's when you know you've found a very stable and highly optimized route.


ADDITIONAL OPTIONS
------------------
* Copy Route: After a route is calculated, a copy button will appear. This will copy the ordered list of systems to your clipboard in the required in-game format.
