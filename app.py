from flask import Flask, jsonify, request
from models import Policyholder, Policy, Claim

app = Flask(__name__)

# === Policyholder Routes ===
@app.route('/policyholders', methods=['POST'])
def create_policyholder():
    data = request.get_json()
    policyholder_id = data.get('policyholder_id')
    name = data.get('name')
    policyholder = Policyholder.create(policyholder_id, name)
    if policyholder:
        return jsonify(policyholder), 201
    return jsonify({"error": "Policyholder already exists or invalid data"}), 400

@app.route('/policyholders', methods=['GET'])
def get_policyholders():
    return jsonify(Policyholder.get_all())

@app.route('/policyholders/<int:policyholder_id>', methods=['GET'])
def get_policyholder(policyholder_id):
    policyholder = Policyholder.get(policyholder_id)
    if policyholder:
        return jsonify(policyholder)
    return jsonify({"error": "Policyholder not found"}), 404

@app.route('/policyholders/<int:policyholder_id>', methods=['PUT'])
def update_policyholder(policyholder_id):
    data = request.get_json()
    updated = Policyholder.update(policyholder_id, data.get('name'))
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Policyholder not found"}), 404

@app.route('/policyholders/<int:policyholder_id>', methods=['DELETE'])
def delete_policyholder(policyholder_id):
    if Policyholder.delete(policyholder_id):
        return jsonify({"message": "Policyholder deleted successfully"}), 200
    return jsonify({"error": "Policyholder not found"}), 404

# === Policy Routes ===
@app.route('/policies', methods=['POST'])
def create_policy():
    data = request.get_json()
    policy = Policy.create(**data)
    if policy:
        return jsonify(policy), 201
    return jsonify({"error": "Invalid policyholder or policy already exists"}), 400

@app.route('/policies', methods=['GET'])
def get_policies():
    return jsonify(Policy.get_all())

@app.route('/policies/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):
    policy = Policy.get(policy_id)
    if policy:
        return jsonify(policy)
    return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/<int:policy_id>', methods=['PUT'])
def update_policy(policy_id):
    data = request.get_json()
    updated = Policy.update(policy_id, data.get('policy_type'), data.get('policy_amount'))
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Policy not found"}), 404

@app.route('/policies/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    if Policy.delete(policy_id):
        return jsonify({"message": "Policy deleted successfully"}), 200
    return jsonify({"error": "Policy not found"}), 404

# === Claim Routes ===
@app.route('/claims', methods=['POST'])
def create_claim():
    data = request.get_json()
    claim = Claim.create(**data)
    if isinstance(claim, dict) and "error" in claim:
        return jsonify(claim), 400
    return jsonify(claim), 201

@app.route('/claims', methods=['GET'])
def get_claims():
    return jsonify(Claim.get_all())

@app.route('/claims/<int:claim_id>', methods=['GET'])
def get_claim(claim_id):
    claim = Claim.get(claim_id)
    if claim:
        return jsonify(claim)
    return jsonify({"error": "Claim not found"}), 404

@app.route('/claims/<int:claim_id>', methods=['PUT'])
def update_claim(claim_id):
    data = request.get_json()
    updated = Claim.update(claim_id, data.get('amount'), data.get('status'))
    if isinstance(updated, dict) and "error" in updated:
        return jsonify(updated), 400
    if updated:
        return jsonify(updated)
    return jsonify({"error": "Claim not found"}), 404

@app.route('/claims/<int:claim_id>', methods=['DELETE'])
def delete_claim(claim_id):
    if Claim.delete(claim_id):
        return jsonify({"message": "Claim deleted successfully"}), 200
    return jsonify({"error": "Claim not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
