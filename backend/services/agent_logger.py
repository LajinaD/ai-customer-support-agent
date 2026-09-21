from datetime import datetime


def create_agent_log():
    return {
        "started_at": datetime.utcnow().isoformat(),
        "tools": [],
        "tool_count": 0,
        "errors": [],
    }


def log_tool_call(
    log: dict,
    tool_name: str,
    arguments: dict,
    duration_ms: float,
    success: bool,
):
    log["tools"].append({
        "tool": tool_name,
        "arguments": arguments,
        "duration_ms": round(duration_ms, 2),
        "success": success,
    })

    log["tool_count"] += 1


def log_error(
    log: dict,
    error: str,
):
    log["errors"].append(error)


def finish_agent_log(log: dict):
    log["finished_at"] = datetime.utcnow().isoformat()

    return log