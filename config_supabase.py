import os
from supabase import create_client, Client

class SupabaseConfig:
    """Supabase configuration and client setup"""
    
    def __init__(self):
        self.url = os.environ.get('SUPABASE_URL')
        self.service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')  # Use service key for server operations
        self.anon_key = os.environ.get('SUPABASE_ANON_KEY')
        self.db_password = os.environ.get('SUPABASE_DB_PASSWORD')
        
        # Create client with service role key for server-side operations
        if self.url and self.service_key:
            self.client: Client = create_client(self.url, self.service_key)
        elif self.url and self.anon_key:
            self.client: Client = create_client(self.url, self.anon_key)
        else:
            raise ValueError("Missing Supabase URL or API key")
    
    def get_client(self) -> Client:
        """Get Supabase client instance"""
        return self.client
    
    def get_database_url(self) -> str:
        """Get PostgreSQL connection URL for SQLAlchemy"""
        if not self.url or not self.db_password:
            return ""
        # Extract project ref from URL for connection string
        project_ref = self.url.split('//')[1].split('.')[0]
        return f"postgresql://postgres.{project_ref}:{self.db_password}@aws-0-us-east-1.pooler.supabase.com:5432/postgres"

# Global Supabase instance
supabase_config = SupabaseConfig()
supabase = supabase_config.get_client()