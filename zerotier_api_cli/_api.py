import requests

ZT_API_BASE = "https://api.zerotier.com/api/v1"


def _api_headers(token):
    return {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }


def fetch_members(token, network_id):
    """Fetch all members of the ZeroTier network."""
    url = f"{ZT_API_BASE}/network/{network_id}/member"
    resp = requests.get(url, headers=_api_headers(token))
    resp.raise_for_status()
    return resp.json()


def authorize_member(token, network_id, member_id):
    """Authorize a single member by ID."""
    url = f"{ZT_API_BASE}/network/{network_id}/member/{member_id}"
    payload = {"config": {"authorized": True}}
    resp = requests.post(url, headers=_api_headers(token), json=payload)
    resp.raise_for_status()
    return resp.json()


def remove_member(token, network_id, member_id):
    """Remove a single member by ID."""
    url = f"{ZT_API_BASE}/network/{network_id}/member/{member_id}"
    resp = requests.delete(url, headers=_api_headers(token))
    resp.raise_for_status()
    return True
