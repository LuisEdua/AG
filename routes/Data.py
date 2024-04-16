from flask import Blueprint, request
from controllers import Data

DataRoutes = Blueprint("/data/", __name__)

@DataRoutes.route('/analisis', methods=['POST'])
def inciarAnalisis():
    
    req: object = request.get_json();               
    
    data = Data.init(req)
    
    
    
    return {"data":data}, 200


