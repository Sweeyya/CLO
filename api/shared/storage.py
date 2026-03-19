import os, json, uuid, datetime
from azure.storage.queue import QueueClient
from azure.data.tables import TableServiceClient, UpdateMode

QUEUE_NAME = os.getenv("QUEUE_NAME", "clo-deferred")
TABLE_CONN = os.getenv("TABLE_CONN", "UseDevelopmentStorage=true")
TABLE_NAME = os.getenv("TABLE_NAME", "CLORequests")

def _queue_client():
    return QueueClient.from_connection_string(TABLE_CONN, QUEUE_NAME)

def _table_client():
    svc = TableServiceClient.from_connection_string(TABLE_CONN)
    try:
        svc.create_table_if_not_exists(TABLE_NAME)
    except Exception:
        pass
    return svc.get_table_client(TABLE_NAME)

def new_request(prompt, priority, region, decision, eta=None):
    rid = str(uuid.uuid4())
    tc = _table_client()
    entity = {
        "PartitionKey": region or "default",
        "RowKey": rid,
        "promptPreview": prompt[:120],
        "priority": priority,
        "modelPlan": decision["model"],
        "maxTokens": decision["max_tokens"],
        "intensityPlan": decision["intensity"],
        "status": "queued" if eta else "running",
        "etaUtc": eta.isoformat() if eta else None,
        "createdUtc": datetime.datetime.utcnow().isoformat()
    }
    tc.create_entity(entity=entity)
    return rid

def enqueue_request(rid: str, payload: dict, visibility_timeout_sec: int):
    qc = _queue_client()
    qc.create_queue()
    qc.send_message(json.dumps({"rid": rid, **payload}), visibility_timeout=visibility_timeout_sec)

def complete_request(rid: str, region: str, model_used: str, intensity: int, tokens_out: int):
    tc = _table_client()
    entity = tc.get_entity(partition_key=region or "default", row_key=rid)
    entity.update({
        "status": "done",
        "modelUsed": model_used,
        "intensityReal": intensity,
        "tokensOut": tokens_out,
        "completedUtc": datetime.datetime.utcnow().isoformat()
    })
    tc.update_entity(mode=UpdateMode.MERGE, entity=entity)
