class TestCase:
    def __init__(self, container_width: int, container_height: int, radii: list[float], masses: list[int]):
        self.container_width = container_width
        self.container_height = container_height
        self.radii = radii
        self.masses = masses



test_cases = {
    "b_01_three_identical" : TestCase(10, 10, [1.0, 1.0, 1.0], [10, 10, 10]),
    "b_02_two_sizes" : TestCase(12, 10, [1.5, 1.5, 1.0, 2.0], [20, 20, 15, 15]),
    "b_03_varied_sizes" : TestCase(15, 12, [1.75, 1.5, 1.25, 1.25, 1.0], [25, 20, 18, 18, 15]),
    "c_01_tight_packing" : TestCase(15, 15, [2.0, 1.75, 1.75, 1.5, 1.5, 1.25, 1.25, 1.0], [35, 30, 30, 25, 25, 20, 20, 15]),
    "c_02_weight_balance" : TestCase(18, 14, [1.5, 1.5, 1.25, 1.25, 1.25, 1.25, 1.75, 1.75], [80, 80, 10, 10, 10, 10, 60, 60]),
    "c_03_many_small" : TestCase(20, 15, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]),
    "c_04_mixed_constraints" : TestCase(20, 20, [2.5, 2.25, 2.0, 1.75, 1.75, 1.5, 1.5, 1.25, 1.25, 1.0], [50, 45, 40, 35, 35, 30, 30, 25, 25, 20])
}