import fire

import script 
import model
import script.script
import server

class GlucodeComaPrediction(object):
    """CLI implementation."""

    def generate(self, sample: str):
        script.script.run(sample)
    

    def build(self, data: str, sample: str):
        model.model.run(data, sample)
    
    def start(self, sample: str):
        server.server.run(sample)

if __name__ == '__main__':
  fire.Fire(GlucodeComaPrediction)