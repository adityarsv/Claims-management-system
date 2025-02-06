class Policyholder:
    policyholders = {}

    @classmethod
    def create(cls, policyholder_id, name):
        if policyholder_id in cls.policyholders:
            return None
        policyholder = {'policyholder_id': policyholder_id, 'name': name}
        cls.policyholders[policyholder_id] = policyholder
        return policyholder

    @classmethod
    def get_all(cls):
        return list(cls.policyholders.values())

    @classmethod
    def get(cls, policyholder_id):
        return cls.policyholders.get(policyholder_id)

    @classmethod
    def update(cls, policyholder_id, name=None):
        policyholder = cls.policyholders.get(policyholder_id)
        if not policyholder:
            return None
        if name:
            policyholder['name'] = name
        return policyholder

    @classmethod
    def delete(cls, policyholder_id):
        return cls.policyholders.pop(policyholder_id, None) is not None


class Policy:
    policies = {}

    @classmethod
    def create(cls, policy_id, policyholder_id, policy_type, policy_amount):
        if policy_id in cls.policies:
            return None
        policyholder = Policyholder.get(policyholder_id)
        if not policyholder:
            return None
        policy = {'policy_id': policy_id, 'policyholder_id': policyholder_id,
                  'policy_type': policy_type, 'policy_amount': policy_amount,
                  'policyholder_name': policyholder['name']}
        cls.policies[policy_id] = policy
        return policy

    @classmethod
    def get_all(cls):
        return list(cls.policies.values())

    @classmethod
    def get(cls, policy_id):
        return cls.policies.get(policy_id)

    @classmethod
    def update(cls, policy_id, policy_type=None, policy_amount=None):
        policy = cls.policies.get(policy_id)
        if not policy:
            return None
        if policy_type:
            policy['policy_type'] = policy_type
        if policy_amount is not None:
            policy['policy_amount'] = policy_amount
        return policy

    @classmethod
    def delete(cls, policy_id):
        return cls.policies.pop(policy_id, None) is not None


class Claim:
    claims = {}

    @classmethod
    def create(cls, claim_id, policy_id, amount):
        policy = Policy.get(policy_id)
        if not policy:
            return {"error": "Policy does not exist"}
        if amount <= 0:
            return {"error": "Claim amount must be a positive number."}
        if amount > policy['policy_amount']:
            return {"error": "Claim amount cannot exceed the policy amount."}

        claim = {'claim_id': claim_id, 'policy_id': policy_id, 'amount': amount,
                 'status': 'Pending', 'policy_type': policy['policy_type'],
                 'policyholder_name': policy['policyholder_name'],
                 'policyholder_id': policy['policyholder_id']}
        cls.claims[claim_id] = claim
        return claim

    @classmethod
    def get_all(cls):
        return list(cls.claims.values())

    @classmethod
    def get(cls, claim_id):
        return cls.claims.get(claim_id)

    @classmethod
    def update(cls, claim_id, amount=None, status=None):
        claim = cls.claims.get(claim_id)
        if not claim:
            return None
        if amount is not None:
            if amount <= 0:
                return {"error": "Claim amount must be a positive number."}
            if amount > Policy.policies[claim['policy_id']]['policy_amount']:
                return {"error": "Claim amount cannot exceed the policy amount."}
            claim['amount'] = amount
        if status:
            if status not in ['Pending', 'Approved', 'Rejected']:
                return {"error": "Invalid status. Allowed values: 'Pending', 'Approved', 'Rejected'."}
            claim['status'] = status
        return claim

    @classmethod
    def delete(cls, claim_id):
        return cls.claims.pop(claim_id, None) is not None
