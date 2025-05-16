def log_action(action, by_user, target_user, reason):
    print(f"[{action.upper()}] {by_user} -> {target_user} | Reason: {reason}")