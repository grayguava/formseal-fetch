# fsf/providers/supabase/__init__.py
# Supabase provider

from fsf.providers import BaseProvider
from fsf.providers.supabase.engine import run


class SupabaseProvider(BaseProvider):

    name = "supabase"

    def fetch(self, config):
        return run(config)


Provider = SupabaseProvider