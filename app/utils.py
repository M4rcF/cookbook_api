def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    from redis_config import jwt_redis_blocklist
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
