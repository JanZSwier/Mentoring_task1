import json

from covid import compute_answer


def test_compute_answer():
    assert json.dumps({"recovered":

                           5.0, "sick": 4.0}, indent=1) == compute_answer(
        population=1000, confirmed_cases=100, recovered_people=50, dead_people=10
    )
