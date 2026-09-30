"""Unit tests for sensor acquisition boundary."""
import pytest

from edge.sensors.acquisition import SensorAcquisitionService
from edge.sensors.rpm import SimulatedRpmSensor
from edge.sensors.temperature import ReplayTemperatureSensor, SimulatedTemperatureSensor
from edge.sensors.vibration import ReplayVibrationSensor, SimulatedVibrationSensor
from shared.contracts import SchemaName, validate_contract


def test_simulated_sensors_produce_numeric_readings() -> None:
    vib = SimulatedVibrationSensor(baseline=0.4, noise=0.02)
    temp = SimulatedTemperatureSensor(baseline=55.0)
    rpm = SimulatedRpmSensor(target_rpm=3000.0)

    assert isinstance(vib.read(), float)
    assert isinstance(temp.read(), float)
    assert isinstance(rpm.read(), float)
    assert 0.3 <= vib.read() <= 0.5
    assert 50.0 <= temp.read() <= 60.0
    assert 2900.0 <= rpm.read() <= 3100.0


def test_replay_sensors_replay_exact_sequence() -> None:
    expected = [0.1, 0.2, 0.35, 0.4]
    replay = ReplayVibrationSensor(expected, loop=False)

    for val in expected:
        assert replay.read() == val

    # Non-looping returns last element
    assert replay.read() == 0.4


def test_replay_sensor_rejects_empty_sequence() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        ReplayTemperatureSensor([])


def test_sensor_acquisition_service_produces_contract_samples() -> None:
    service = SensorAcquisitionService(device_id="demo-edge-01")
    service.register_sensor(
        sensor_id="vib-01",
        sensor_type="vibration",
        unit="g",
        calibration_version="cal-1.0",
        reader=SimulatedVibrationSensor(),
    )
    service.register_sensor(
        sensor_id="temp-01",
        sensor_type="temperature",
        unit="degC",
        calibration_version="cal-1.0",
        reader=SimulatedTemperatureSensor(),
    )

    sample1 = service.acquire_sample("vib-01")
    sample2 = service.acquire_sample("vib-01")

    # Sequence monotonicity
    assert sample1["sequence"] == 0
    assert sample2["sequence"] == 1
    assert sample1["sensor_id"] == "vib-01"
    assert sample1["device_id"] == "demo-edge-01"

    # Schema validation
    valid1, err1 = validate_contract(sample1, SchemaName.SENSOR_SAMPLE)
    assert valid1, err1

    valid2, err2 = validate_contract(sample2, SchemaName.SENSOR_SAMPLE)
    assert valid2, err2


def test_sensor_acquisition_acquire_all() -> None:
    service = SensorAcquisitionService()
    service.register_sensor("vib-01", "vibration", "g", "v1", SimulatedVibrationSensor())
    service.register_sensor("temp-01", "temperature", "degC", "v1", SimulatedTemperatureSensor())
    service.register_sensor("rpm-01", "rpm", "rpm", "v1", SimulatedRpmSensor())

    all_samples = service.acquire_all()
    assert len(all_samples) == 3
    for s in all_samples:
        valid, err = validate_contract(s, SchemaName.SENSOR_SAMPLE)
        assert valid, err


def test_sensor_acquisition_unregistered_sensor_raises() -> None:
    service = SensorAcquisitionService()
    with pytest.raises(KeyError, match="not registered"):
        service.acquire_sample("nonexistent-sensor")
