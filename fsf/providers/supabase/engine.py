# fsf/providers/supabase/engine.py
# Supabase engine

from fsf.providers.supabase.storage import fetch as supabase_fetch


def run(config):
    ref = config.get("project_ref")
    token = config.get("token")
    table = config.get("table")
    if not ref or not token:
        raise ValueError("project_ref and token are required")
    if not table:
        raise ValueError("table is required")
    return supabase_fetch(ref=ref, token=token, table=table)