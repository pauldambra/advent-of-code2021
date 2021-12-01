from typing import Optional, Iterator


def check_sonar_readings_for_increases(sonar_readings: Iterator[str]) -> int:
    previous: Optional[int] = None
    increases = 0
    for reading in [int(s) for s in sonar_readings]:
        if previous:
            if reading - previous > 0:
                increases += 1

        previous = reading
    return increases


def test_example_sonar():
    sonar_readings = """199
200
208
210
200
207
240
269
260
263"""

    increases = check_sonar_readings_for_increases(iter(sonar_readings.splitlines()))

    assert increases == 7


def test_file_input():
    with open('part1.input', 'r', newline='\n') as f:
        increases = check_sonar_readings_for_increases(iter(f.readlines()))

        assert increases == 1374
