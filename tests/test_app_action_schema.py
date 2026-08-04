"""Regression coverage for app_action schema and seed lookup."""

from pathlib import Path
import yaml


def _app_action_config():
    data = yaml.safe_load(Path("nchantrs/models/_data_/applicationmodels.yaml").read_text())
    return data["NchantdPantiesModel"]["dstruct"]["database"]["objects"]["table"]["app_action"]


def test_app_action_schema_defines_position_column_for_ordered_reads():
    config = _app_action_config()
    columns = [column["name"] for column in config["columns"]]
    assert "position_int" in columns


def test_show_pane_left_seed_matches_app_action_schema_width():
    config = _app_action_config()
    record = next(row for row in config["system_records"] if row[1] == "show_pane_left")
    assert len(record) == len(config["columns"])
    assert isinstance(record[-1], int)
