from flask import Blueprint, jsonify, request
from crud import *

manage_customers = Blueprint('manage_customers', __name__)

@manage_customers.route('/customers', methods=['GET','POST','DELETE','PUT'])
def manageCustomers():
    if request.method == 'GET':

        customer_id = request.args.get('customer_id')
        
        if customer_id:
            customer = find_customer_by_id(customer_id)
            if customer:
                return jsonify(customer)  # Return the book details as JSON
            else:
                return jsonify({"message": "Customer not found"}), 404
            
        customer_name = request.args.get('customer_name')

        if customer_name:
            customer = find_customer_by_name(customer_name)
            if customer:  
                return jsonify(customer) 
            else:
                return jsonify({"message": "Customer not found"}), 404
            
        filter_type = request.args.get('filter', 'active')
        
        if filter_type == 'active':
            active_customers = display_active_customers()
            return jsonify(active_customers)
        
        if filter_type == 'inactive':
            inactive_customers = display_inactive_customers()
            return jsonify(inactive_customers)
        
        if filter_type == 'history':
            all_customers = display_all_customers()
            return jsonify(all_customers)
    
    if request.method == 'POST':
        data = request.get_json()
        customerName = data.get('name')
        customerCity = data.get('city')
        customerAge = data.get('age')

        add_new_customer(customerName, customerCity, customerAge)
        return jsonify({"message": "New Customer was added"}), 201
    
    if request.method == 'PUT':
        update_customer()
        return jsonify({"message": "Customer was updated successfully!"}), 200
    
    if request.method== 'DELETE':

        filter_type = request.args.get('action')

        if filter_type == 'restore':
            restore_customer()
            return jsonify({"message": "Customer was restored succussfully!"}), 200
        
        delete_customer()
        return jsonify({"message": "Customer's Status changed to innactive"}), 200