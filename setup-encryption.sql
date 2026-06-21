CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Safely decrypt; returns raw value if not yet encrypted (migration grace)
CREATE OR REPLACE FUNCTION _try_decrypt(val text, enc_pass text)
RETURNS text LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  IF val IS NULL OR val = '' THEN RETURN ''; END IF;
  BEGIN
    RETURN pgp_sym_decrypt(decode(val,'base64'), enc_pass);
  EXCEPTION WHEN OTHERS THEN RETURN val; END;
END; $$;

-- Encrypt and upsert keys (passphrase never leaves the server function)
CREATE OR REPLACE FUNCTION upsert_user_keys(
  p_user_id uuid, p_claude text, p_openai text, p_apify text,
  p_ghl text, p_ghl_loc text, p_provider text
) RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE enc text := '1cd873eb7b17c06ec69a47d845e8509ed0882e7768b233e23d8e72b8d975bf02';
BEGIN
  INSERT INTO user_keys(user_id,claude_key,openai_key,apify_key,ghl_key,ghl_location_id,ai_provider,updated_at)
  VALUES (p_user_id,
    CASE WHEN p_claude  <> '' THEN encode(pgp_sym_encrypt(p_claude, enc),'base64') ELSE '' END,
    CASE WHEN p_openai  <> '' THEN encode(pgp_sym_encrypt(p_openai, enc),'base64') ELSE '' END,
    CASE WHEN p_apify   <> '' THEN encode(pgp_sym_encrypt(p_apify,  enc),'base64') ELSE '' END,
    CASE WHEN p_ghl     <> '' THEN encode(pgp_sym_encrypt(p_ghl,    enc),'base64') ELSE '' END,
    CASE WHEN p_ghl_loc <> '' THEN encode(pgp_sym_encrypt(p_ghl_loc,enc),'base64') ELSE '' END,
    p_provider, now())
  ON CONFLICT (user_id) DO UPDATE SET
    claude_key=EXCLUDED.claude_key, openai_key=EXCLUDED.openai_key,
    apify_key=EXCLUDED.apify_key, ghl_key=EXCLUDED.ghl_key,
    ghl_location_id=EXCLUDED.ghl_location_id, ai_provider=EXCLUDED.ai_provider, updated_at=now();
END; $$;

-- Fetch and decrypt keys
CREATE OR REPLACE FUNCTION get_user_keys(p_user_id uuid)
RETURNS TABLE(claude_key text,openai_key text,apify_key text,ghl_key text,ghl_location_id text,ai_provider text)
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE enc text := '1cd873eb7b17c06ec69a47d845e8509ed0882e7768b233e23d8e72b8d975bf02'; raw user_keys%ROWTYPE;
BEGIN
  SELECT * INTO raw FROM user_keys WHERE user_keys.user_id = p_user_id;
  IF NOT FOUND THEN RETURN; END IF;
  RETURN QUERY SELECT
    _try_decrypt(raw.claude_key,enc), _try_decrypt(raw.openai_key,enc),
    _try_decrypt(raw.apify_key, enc), _try_decrypt(raw.ghl_key,enc),
    _try_decrypt(raw.ghl_location_id,enc), raw.ai_provider;
END; $$;

GRANT EXECUTE ON FUNCTION upsert_user_keys TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_keys     TO authenticated;
GRANT EXECUTE ON FUNCTION _try_decrypt      TO authenticated;
