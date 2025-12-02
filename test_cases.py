class TestCase:
    def __init__(self, container_width: int, container_height: int, radii: list[float], masses: list[int]):
        self.container_width = container_width
        self.container_height = container_height
        self.radii = radii
        self.masses = masses



test_cases = {
    "b01_3_identical" : TestCase(10, 10, [1.0, 1.0, 1.0], [10, 10, 10]),
    "b02_2_sizes" : TestCase(12, 10, [1.5, 1.5, 1.0, 2.0], [20, 20, 15, 15]),
    "b03_varied" : TestCase(15, 12, [1.75, 1.5, 1.25, 1.25, 1.0], [25, 20, 18, 18, 15])
}