import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.load import save_to_json

def test_save_to_json_creates_file(tmp_path):
    test_data = [{"title": "Sample", "identifier": "123"}]
    output_file = tmp_path / "test_output.json"
    save_to_json(test_data, str(output_file))
    assert output_file.exists()