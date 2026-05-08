import json
import os
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def current_month():
    return datetime.now().strftime("%Y-%m")


def handler(request):
    query = request.get("query", {}) or {}
    month = query.get("month", current_month())

    result = (
        supabase.table("transactions")
        .select("*")
        .filter("date", "gte", f"{month}-01")
        .filter("date", "lte", f"{month}-31")
        .order("date", desc=True)
        .execute()
    )

    return _json({"transactions": result.data})


def _json(data, status=200):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data),
    }
