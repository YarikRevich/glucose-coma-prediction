import fire

import script 
import model
import script.script
import server

class GlucodeComaPrediction(object):
    """CLI implementation."""
    
    def generate(self, sample: str):
        """Performs train and example data generation."""
        
        script.script.run(sample)
        
    def build(self, data: str, sample: str):
        """Performs models build operation."""
        
        model.model.run(data, sample)
    
    def start(self, sample: str):
        """Performs start of server application."""
        
        server.server.run(sample)

if __name__ == '__main__':
  fire.Fire(GlucodeComaPrediction)