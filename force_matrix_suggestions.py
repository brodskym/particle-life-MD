import numpy as np

# =====================================================================
# 1. THE CYCLIC "CHASING SNAKE" (Predator-Prey-Scavenger)
# =====================================================================
# Row i feels attraction/repulsion from Column j
# Order: [Red, Green, Blue]
snake_interaction_matrix = np.array([
    [ 0.1,  0.4, -0.4],  # Red is happy alone, chased by Green, runs from Blue
    [-0.4,  0.1,  0.4],  # Green runs from Red, happy alone, chased by Blue
    [ 0.4, -0.4,  0.1]   # Blue chased by Red, runs from Green, happy alone
], dtype=np.float32)


# =====================================================================
# 2. BIOLOGICAL "CELLS" (Nucleus & Membrane)
# =====================================================================
cell_interaction_matrix = np.array([
    [ 0.6,  0.0,  0.0],  # Red clumps tight, completely ignores Green & Blue
    [ 0.5, -0.2,  0.0],  # Green seeks Red, repels self to wrap around Red
    [ 0.0,  0.2,  0.1]   # Blue ignores Red, slowly migrates toward Green
], dtype=np.float32)


# =====================================================================
# 3. THE DANCING ORBITALS (Spiraling Galaxies)
# =====================================================================
spiral_galaxy_interaction_matrix = np.array([
    [-0.1,  0.3, -0.2],  # Red self-repels, strongly pulls Green, avoids Blue
    [-0.2, -0.1,  0.3],  # Green avoids Red, self-repels, strongly pulls Blue
    [ 0.3, -0.2, -0.1]   # Blue strongly pulls Red, avoids Green, self-repels
], dtype=np.float32)


# =====================================================================
# 4. MITOSIS & EVOLVING SLIME MOLD
# =====================================================================
slime_interaction_matrix = np.array([
    [ 0.30, -0.20,  0.40], # Red interaction
    [ 0.40,  0.25, -0.30], # Green interaction
    [-0.20,  0.35,  0.10]  # Blue interaction
], dtype=np.float32)
