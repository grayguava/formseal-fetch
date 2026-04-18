# Supabase provider

from cli.providers import Provider
from cli.providers.supabase.storage import fetch as supabase_fetch


class SupabaseProvider(Provider):

    name = "supabase"
    display_name = "🐘 Supabase"
    storage_type = "postgres"

    @property
    def storage_label(self):
        return "PostgreSQL"

    @property
    def description(self):
        return f"{self.storage_label} database"

    def get_config_schema(self):
        return {
            "project_ref": {
                "required": True,
                "description": "Project Reference",
                "sensitive": False
            },
            "table": {
                "required": True,
                "description": "Table Name",
                "sensitive": False
            }
        }

    def fetch(self, config):
        ref = config.get("project_ref")
        token = config.get("token")
        table = config.get("table")
        if not ref or not token:
            raise ValueError("project_ref and token are required")
        if not table:
            raise ValueError("table is required")
        return supabase_fetch(ref=ref, token=token, table=table)


Provider = SupabaseProvider