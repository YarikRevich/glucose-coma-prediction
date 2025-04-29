import sys
import numpy as np
import pickle

def main(file: str) -> None:
    model = pickle.load(open(f"{file}.random_forest", "rb"))
    
    q = [[588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,90,85,75,58,41,46,45,42,40,50,42]]
    
    y_pred = model.predict(q)
    print(y_pred)
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Not enough arguments provided!")
    
    main(sys.argv[1])