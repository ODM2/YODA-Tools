from DataLoader.domain.Inputs.yamlInput import yamlInput
import os
curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class TestYaml:
    def setup(self):
        self.yi = yamlInput()

    def test_parse_ts(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_ts.yaml')
        self.yi.parse(file_path)

        session = self.yi.sendODM2Session()

        assert session != None
        from odm2api.ODM2.models import People, SamplingFeatures
        assert len(session.query(People).all()) > 0
        assert len(session.query(SamplingFeatures).all()) > 0
        session.close()

    def test_parse_specimen(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_specimen_ts.yaml')

        self.yi.parse(file_path)
        session = self.yi.sendODM2Session()

        assert session != None
        from odm2api.ODM2.models import People, SamplingFeatures
        assert len(session.query(People).all()) > 0
        assert len(session.query(SamplingFeatures).all()) > 0
        session.close()



