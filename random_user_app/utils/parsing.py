import re

def parse_message(message: str) -> dict:
    match = re.match(r"^(.*?)\nstatus:\s*(\w+)", message)
    if not match:
        return {'msg': message, 'status': ''}
    
    msg, status = match.groups()
    return {"msg": msg.strip(), "status": status.strip()}