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
    start = query.get("start")
    end = query.get("end", current_month())

    if not start:
        y, m = map(int, end.split("-"))
        m -= 2
        if m <= 0:
            m += 12
            y -= 1
        start = f"{y}-{m:02d}"

    result = (
        supabase.table("transactions")
        .select("*")
        .filter("date", "gte", f"{start}-01")
        .filter("date", "lte", f"{end}-31")
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
