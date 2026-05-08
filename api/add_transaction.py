import json
import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def handler(request):
    body_raw = request.get("body") or "{}"
    try:
        data = json.loads(body_raw)
    except Exception:
        data = {}

    date = data.get("date")
    category = data.get("category")
    type_ = data.get("type")
    amount = data.get("amount")
    notes = data.get("notes")

    supabase.table("transactions").insert({
        "date": date,
        "category": category,
        "type": type_,
        "amount": amount,
        "notes": notes
    }).execute()

    change = amount if type_ == "income" else -amount
    supabase.table("account_history").insert({
        "date": date,
        "change": change,
        "source": notes or "Transaction"
    }).execute()

    return _json({"status": "success"})


def _json(data, status=200):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data),
    }
