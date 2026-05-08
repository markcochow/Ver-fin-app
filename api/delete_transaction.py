import json
import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def handler(request):
    path = request.get("path", "")
    # Expect path like /api/delete_transaction/123
    try:
        id_ = int(path.rstrip("/").split("/")[-1])
    except Exception:
        return _json({"error": "Invalid id"}, status=400)

    old = (
        supabase.table("transactions")
        .select("*")
        .eq("id", id_)
        .single()
        .execute()
    ).data

    reverse_change = old["amount"] if old["type"] == "expense" else -old["amount"]
    supabase.table("account_history").insert({
        "date": old["date"],
        "change": reverse_change,
        "source": "Delete reversal"
    }).execute()

    supabase.table("transactions").delete().eq("id", id_).execute()

    return _json({"status": "success"})


def _json(data, status=200):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data),
    }
