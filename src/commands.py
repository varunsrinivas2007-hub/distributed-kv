def execute(command, store):
    parts = command.split()

    if not parts:
        return "ERROR empty command"

    action = parts[0].upper()

    if action == "SET":
        if len(parts) != 3:
            return "ERROR usage: SET <key> <value>"

        key = parts[1]
        value = parts[2]

        store.set(key, value)

        return "OK"

    if action == "GET":
        if len(parts) != 2:
            return "ERROR usage: GET <key>"

        key = parts[1]

        value = store.get(key)

        if value is None:
            return "(nil)"

        return value

    return "ERROR unknown command"
